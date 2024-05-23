from functools import lru_cache

from aiohttp import ClientConnectorError
from elasticsearch import exceptions

from db.elastic import get_elastic_service
from db.redis_db import DataCache
from models.genre import Genre

from src.db.backoff_decorator import backoff


class GenreService(DataCache):
    def __init__(self):
        DataCache.__init__(self, Genre, )

        self._elastic_service = get_elastic_service(index='genres', schema=Genre)

    @backoff((exceptions.ConnectionError, ClientConnectorError), 1, 2, 100, 10)
    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre_cache = f'g_{genre_id}'
        genre = await self.get_from_cache(genre_cache)
        if genre:
            return genre

        genre = await self._elastic_service.get_one(document_id=genre_id)
        if not genre:
            return genre
        await self.put_to_cache(genre, genre_cache)
        return genre

    @backoff((exceptions.ConnectionError, ClientConnectorError), 1, 2, 100, 10)
    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            query: str = None,
    ) -> list[Genre] | None:
        genre_cache = f'g_{page_number}{page_size}{query}'
        genres = await self.get_from_cache(genre_cache)
        if genres:
            return genres

        body = {
            'query': {'match_all': {}},
        }
        genres = await self._elastic_service.get_list(body=body, page_number=page_number, page_size=page_size)
        if not genres:
            return None
        await self.put_to_cache(genres, genre_cache)
        return genres


@lru_cache()
def get_genre_service() -> GenreService:
    return GenreService()
