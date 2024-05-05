from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis_db import get_redis
from models.genre import Genre, GenreMainData

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # async def get_by_id(self, film_id: str) -> Optional[Film]:
    async def get_genre(self, genre_id: str = None, n_elem: int = 100, page: int = 1) -> Optional[Genre]:

        # Пока что я кэширование отключил
        # film = await self._film_from_cache(film_id)
        genre = None
        if not genre:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            genre = await self._get_genre_from_elastic(genre_id, n_elem, page)
            if not genre:
                return None
            # Сохраняем фильм в кеш (Пока отключил)
            # await self._put_film_to_cache(film)

        return genre

    async def _get_genre_from_elastic(self, genre_id: str = None, n_elem: int = 50, page: int = 1) -> Optional[Genre]:
        try:
            if genre_id:
                doc = await self.elastic.get(index='genres', id=genre_id)
                return Genre(**doc['_source'])

            else:
                body_query = {
                    'query': {'match_all': {}},
                }

            start_idx = 1
            if not page == 1:
                start_idx = n_elem * page

            doc = await self.elastic.search(
                index='genres',
                body=body_query,
                size=n_elem,
                from_=start_idx
            )

            res = list()
            for i in range(len(doc['hits']['hits'])):
                res.append(GenreMainData(**doc['hits']['hits'][i]['_source']))

            return res

        except NotFoundError:
            return None

    async def _genre_from_cache(self, film_id: str) -> Optional[Genre]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Genre.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Genre):
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
