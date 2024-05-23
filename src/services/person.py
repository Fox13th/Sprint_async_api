from functools import lru_cache

from aiohttp import ClientConnectorError
from elasticsearch import exceptions

from db.elastic import get_elastic_service
from db.redis_db import DataCache
from models.person import Person

from db.backoff_decorator import backoff


class PersonService(DataCache):
    def __init__(self):
        DataCache.__init__(self, Person, )

        self._elastic_service = get_elastic_service(index='persons', schema=Person)

    @backoff((exceptions.ConnectionError, ClientConnectorError), 1, 2, 100, 10)
    async def get_by_id(self, person_id: str) -> Person | None:

        person_cache = f'p_{person_id}'
        person = await self.get_from_cache(person_cache)
        if person:
            return person

        person = await self._elastic_service.get_one(document_id=person_id)
        if not person:
            return None
        await self.put_to_cache(person, person_cache)
        return person

    @backoff((exceptions.ConnectionError, ClientConnectorError), 1, 2, 100, 10)
    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            query: str = None,
    ) -> list[Person] | None:

        person_cache = f'p_{page_number}{page_size}{query}'
        persons = await self.get_from_cache(person_cache)
        if persons:
            return persons

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
        persons = await self._elastic_service.get_list(body=body, page_number=page_number, page_size=page_size)
        if not persons:
            return None
        await self.put_to_cache(persons, person_cache)
        return persons


@lru_cache()
def get_person_service() -> PersonService:
    return PersonService()
