from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from orjson import orjson
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis_db import get_redis
from models.film import Genre, GenreMainData

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.idx = 'genres'

    async def get_genre(self, genre_id: str = None, n_elem: int = 100, page: int = 1) -> Genre | None:

        genre_cache = f'g_{genre_id}{n_elem}{page}'
        genre = await self._genre_from_cache(genre_cache)

        if not genre:
            genre = await self._get_genre_from_elastic(genre_id, n_elem, page)
            if not genre:
                return None

            await self._put_film_to_cache(genre, genre_cache)

        return genre

    async def _get_genre_from_elastic(self, genre_id: str = None, n_elem: int = 50, page: int = 1) -> Genre | None:
        try:
            if genre_id:
                doc = await self.elastic.get(index=self.idx, id=genre_id)
                return Genre(**doc['_source'])

            else:
                body_query = {
                    'query': {'match_all': {}},
                }

            doc = await self.elastic.search(
                index=self.idx,
                body=body_query,
                size=n_elem,
                from_=(page - 1) * n_elem
            )

            res = list()
            for i in range(len(doc['hits']['hits'])):
                res.append(Genre(**doc['hits']['hits'][i]['_source']))

        except NotFoundError:
            return None

        return res

    async def _genre_from_cache(self, key_cache: str) -> Genre | None:

        data = await self.redis.get(key_cache)
        if not data:
            return None

        try:
            genre = Genre.parse_raw(data)
        except ValueError:
            genre = [Genre.parse_raw(f_data) for f_data in orjson.loads(data)]

        return genre

    async def _put_film_to_cache(self, genre, key_cache):

        if type(genre) == list:
            g_list = [g_data.json() for g_data in genre]
            await self.redis.set(key_cache, orjson.dumps(g_list), GENRE_CACHE_EXPIRE_IN_SECONDS)
        else:
            await self.redis.set(key_cache, genre.json(), GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
