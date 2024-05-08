from functools import lru_cache

import orjson
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
        self.idx = 'movies'

    async def get_film(self, film_id: str = None, query: str = None, n_elem: int = 100, page: int = 1,
                       sort_by: str = None, genre: str = None) -> Film | None:

        film_cache = f'f_{film_id}{query}{n_elem}{page}{sort_by}{genre}'
        film = await self._film_from_cache(film_cache)

        if not film:
            film = await self._get_film_from_elastic(film_id, query, n_elem, page, sort_by, genre)
            if not film:
                return None

            await self._put_film_to_cache(film, film_cache)

        return film

    async def _get_film_from_elastic(self, film_id: str = None, query: str = None, n_elem: int = 100, page: int = 1,
                                     sort_by: str = None, genre: str = None) -> Film | None:
        try:
            if film_id:
                doc = await self.elastic.get(index=self.idx, id=film_id)
                return Film(**doc['_source'])

            elif query:
                body_query = {
                    'query': {
                        'match': {
                            'title': {
                                'query': query,
                                'fuzziness': 'auto'
                            }
                        }
                    },
                }

            else:
                order = 'asc'
                if sort_by[0] == '-':
                    order = 'desc'
                    sort_by = sort_by[1:len(sort_by)]

                match_filter = {'match_all': {}}
                if genre:
                    match_filter = {
                        'query_string': {
                            'default_field': 'genres.id',
                            'query': genre
                        }
                    }

                body_query = {
                    'query': match_filter,
                    'sort': [
                        {
                            sort_by: {
                                'order': order
                            }
                        }
                    ],
                }

            doc = await self.elastic.search(
                index=self.idx,
                body=body_query,
                size=n_elem,
                from_=(page - 1) * n_elem
            )

            res = list()
            for i in range(len(doc['hits']['hits'])):
                res.append(FilmMainData(**doc['hits']['hits'][i]['_source']))

        except NotFoundError:
            return None

        return res

    async def _film_from_cache(self, key_cache: str) -> Film | None:

        data = await self.redis.get(key_cache)
        if not data:
            return None

        try:
            film = Film.parse_raw(data)
        except ValueError:
            film = [FilmMainData.parse_raw(f_data) for f_data in orjson.loads(data)]

        return film

    async def _put_film_to_cache(self, film, key_cache: str):

        if type(film) == list:
            f_list = [f_data.json() for f_data in film]
            await self.redis.set(key_cache, orjson.dumps(f_list), FILM_CACHE_EXPIRE_IN_SECONDS)
        else:
            await self.redis.set(key_cache, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
