from functools import lru_cache

from elasticsearch import exceptions
from aiohttp import ClientConnectorError
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic_service
from db.redis_db import DataCache
from models.film import Film, FilmMainData

from db.backoff_decorator import backoff


class FilmService(DataCache):
    def __init__(self):
        DataCache.__init__(self, Film, FilmMainData)
        self._elastic_service = get_elastic_service(index='movies', schema=Film)

    @backoff((exceptions.ConnectionError, ClientConnectorError), 1, 2, 100, 10)
    async def get_by_id(self, film_id: str) -> Film | None:
        film_cache = f'f_{film_id}'
        film = await self.get_from_cache(film_cache)
        if film:
            return film

        film = await self._elastic_service.get_one(document_id=film_id)
        if not film:
            return None
        await self.put_to_cache(film, film_cache)
        return film

    @backoff((exceptions.ConnectionError, ClientConnectorError), 1, 2, 100, 10)
    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            query: str = None,
            sort_by: str = None,
            genre: str = None
    ) -> list[Film] | None:

        film_cache = f'f_{query}{page_size}{page_number}{sort_by}{genre}'

        films = await self.get_from_cache(film_cache)
        if films:
            return films

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

        films = await self._elastic_service.get_list(body=body, page_number=page_number, page_size=page_size)
        if not films:
            return None
        await self.put_to_cache(films, film_cache)
        return films


@lru_cache()
def get_film_service() -> FilmService:
    return FilmService()
