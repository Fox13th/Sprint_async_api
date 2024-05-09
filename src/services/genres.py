from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis_db import DataCache
from models.genre import Genre


class GenreService(DataCache):
    def __init__(self, elastic: AsyncElasticsearch):
        DataCache.__init__(self, Genre, )

        self.elastic = elastic
        self.idx = 'genres'

    async def get_genre(self, genre_id: str = None, n_elem: int = 100, page: int = 1) -> Genre | list[Genre] | None:

        genre_cache = f'g_{genre_id}{n_elem}{page}'
        genre = await self._film_from_cache(genre_cache)

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


@lru_cache()
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
