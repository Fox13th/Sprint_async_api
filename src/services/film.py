from functools import lru_cache
from models.film import Film, FilmMainData
from services.base import BaseService


class FilmService(BaseService):

    def __init__(self):
        super().__init__(index='movies', schema=Film, main_data_model=FilmMainData)

    async def get_by_id(self, film_id: str) -> Film | None:
        film_cache = f'f_{film_id}'
        return await self._get_one_document(film_id, film_cache)

    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            query: str | None = None,
            sort_by: str | None = None,
            genre: str | None = None
    ) -> list[Film] | None:
        film_cache = f'f_{query}{page_size}{page_number}{sort_by}{genre}'

        if query:
            body = {
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
            if sort_by and sort_by[0] == '-':
                order = 'desc'
                sort_by = sort_by[1:]

            match_filter = {'match_all': {}}
            if genre:
                match_filter = {
                    'query_string': {
                        'default_field': 'genres.id',
                        'query': genre
                    }
                }

            body = {
                'query': match_filter,
                'sort': [
                    {
                        sort_by: {
                            'order': order
                        }
                    }
                ],
            }

        films_list = await self._get_list_documents(
            page_number=page_number,
            page_size=page_size,
            body=body,
            cache_key=film_cache
        )

        return films_list


@lru_cache()
def get_film_service() -> FilmService:
    return FilmService()
