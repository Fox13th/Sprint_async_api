from functools import lru_cache
from models.genre import Genre

from services.base import BaseService


class GenreService(BaseService):
    def __init__(self):
        super().__init__(index='genres', schema=Genre)

    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre_cache = f'g_{genre_id}'
        return await self._get_one_document(genre_id, genre_cache)

    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            query: str = None,
    ) -> list[Genre] | None:
        genre_cache = f'g_{page_number}{page_size}{query}'
        body = {
            'query': {'match_all': {}},
        }
        genres_list = await self._get_list_documents(
            page_number=page_number,
            page_size=page_size,
            body=body,
            cache_key=genre_cache
        )
        return genres_list


@lru_cache()
def get_genre_service() -> GenreService:
    return GenreService()
