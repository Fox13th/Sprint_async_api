from functools import lru_cache
from typing import Optional, List

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from orjson import orjson
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis_db import get_redis
from models.person import Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = 'persons'

    async def get_by_id(self, person_id: str) -> Optional[Person]:

        person_cache = f'p_{person_id}'
        person = await self._person_from_cache(person_cache)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person, person_cache)

        return person

    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            query: str = None,
    ) -> Optional[List[Person]]:

        person_cache = f'p_{page_number}{page_size}{query}'
        person = await self._person_from_cache(person_cache)
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
            await self._put_person_to_cache(person, person_cache)

        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get(index=self.index, id=person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def _person_from_cache(self, key_cache: str) -> Optional[Person]:
        data = await self.redis.get(key_cache)
        if not data:
            return None

        try:
            person = Person.parse_raw(data)
        except ValueError:
            person = [Person.parse_raw(f_data) for f_data in orjson.loads(data)]

        return person

    async def _put_person_to_cache(self, person, key_cache):
        if type(person) == list:
            g_list = [p_data.json() for p_data in person]
            await self.redis.set(key_cache, orjson.dumps(g_list), PERSON_CACHE_EXPIRE_IN_SECONDS)
        else:
            await self.redis.set(key_cache, person.json(), PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
