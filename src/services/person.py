from functools import lru_cache
from models.person import Person
from services.base import BaseService


class PersonService(BaseService):

    def __init__(self):
        super().__init__(index='persons', schema=Person)

    async def get_by_id(self, person_id: str) -> Person | None:

        person_cache = f'p_{person_id}'
        return await self._get_one_document(person_id, person_cache)

    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            query: str = None,
    ) -> list[Person] | None:

        person_cache = f'p_{page_number}{page_size}{query}'
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
        persons_list = await self._get_list_documents(
            page_number=page_number,
            page_size=page_size,
            body=body,
            cache_key=person_cache
        )
        return persons_list


@lru_cache()
def get_person_service() -> PersonService:
    return PersonService()
