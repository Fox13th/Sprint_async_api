from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis_db import DataCache
from models.person import Person


class PersonService(DataCache):
    def __init__(self, elastic: AsyncElasticsearch):
        DataCache.__init__(self, Person, )

        self.elastic = elastic
        self.index = 'persons'

    async def get_by_id(self, person_id: str) -> Person | None:

        person_cache = f'p_{person_id}'
        person = await self._film_from_cache(person_cache)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_film_to_cache(person, person_cache)

        return person

    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            query: str = None,
    ) -> list[Person] | None:

        person_cache = f'p_{page_number}{page_size}{query}'
        person = await self._film_from_cache(person_cache)
        if not person:
            if not query:
                body = {
                    'query': {
                        'match_all': {}
                    }}
            else:
                body = {
                    'query': {
                        'match': {
                            'name': {
                                'query': query,
                                'fuzziness': 'auto'
                            }
                        }
                    },
                }

            docs = await self.elastic.search(
                index=self.index,
                body=body,
                size=page_size,
                from_=((page_number - 1) * page_size)
            )

            person = [Person(**doc['_source']) for doc in docs['hits']['hits']]
            await self._put_film_to_cache(person, person_cache)

        return person

    async def _get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get(index=self.index, id=person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic)
