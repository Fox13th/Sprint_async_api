from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis_db import get_redis
from models.film import Film, FilmMainData

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # async def get_by_id(self, film_id: str) -> Optional[Film]:
    async def get_film(self, film_id: str = None, query: str = None, n_elem: int = 100, page: int = 1,
                       sort_by: str = None) -> Optional[Film]:

        # Пока что я кэширование отключил
        # film = await self._film_from_cache(film_id)
        film = None
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film = await self._get_film_from_elastic(film_id, query, n_elem, page, sort_by)
            if not film:
                return None
            # Сохраняем фильм в кеш (Пока отключил)
            # await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str = None, query: str = None, n_elem: int = 100, page: int = 1,
                                     sort_by: str = None) -> Optional[Film]:
        try:
            if film_id:
                doc = await self.elastic.get(index='movies', id=film_id)
                return Film(**doc['_source'])

            elif query:
                body_query = {
                    'query': {
                        'query_string': {
                            'default_field': 'title',
                            'query': query
                        }
                    },
                }

            else:
                order = 'asc'
                if sort_by[0] == '-':
                    order = 'desc'
                    sort_by = sort_by[1:len(sort_by)]

                body_query = {
                    'query': {
                        'match_all': {}
                    },
                    'sort': [
                        {
                            sort_by: {
                                'order': order
                            }
                        }
                    ],
                }

            doc = await self.elastic.search(
                index='movies',
                body=body_query,
                size=n_elem,
                from_=n_elem * page
            )
            #doc = await self.elastic.mget(index='movies', body=body_query)

            res = list()
            for i in range(n_elem):
                res.append(FilmMainData(**doc['hits']['hits'][i]['_source']))
            return res

        except NotFoundError:
            return None

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
