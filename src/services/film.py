from functools import lru_cache

from elasticsearch import exceptions
from aiohttp import ClientConnectorError
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis_db import DataCache
from models.film import Film, FilmMainData

from src.db.backoff_decorator import backoff


class FilmService(DataCache):
    def __init__(self, elastic: AsyncElasticsearch()):
        DataCache.__init__(self, Film, FilmMainData)

        self.elastic = elastic
        self.idx = 'movies'

    @backoff((exceptions.ConnectionError, ClientConnectorError), 1, 2, 100, 10)
    async def get_film(self, film_id: str = None, query: str = None, n_elem: int = 100, page: int = 1,
                       sort_by: str = None, genre: str = None) -> Film | list[Film] | None:

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


@lru_cache()
def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
