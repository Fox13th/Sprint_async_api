<<<<<<< abc-classes
from abc import ABC, abstractmethod
from typing import Type, TypeVar
from elasticsearch import exceptions
=======
from typing import Type
>>>>>>> main

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel



es: AsyncElasticsearch | None = None
T = TypeVar('T', bound=BaseModel)


class AsyncSearchEngine(ABC):
    @abstractmethod
    async def get_by_id(self, document_id: str) -> T | None:
        pass

    @abstractmethod
    async def get_list(self, body, page_number: int = 1, page_size: int = 50) -> list[T] | None:
        pass


class ElasticAsyncSearchEngine(AsyncSearchEngine):
    def __init__(self, index: str, schema: Type[BaseModel]):
        self._es = es
        self._index = index
        self._schema = schema

<<<<<<< abc-classes
    @backoff((exceptions.ConnectionError,), 1, 2, 100, 10)
    async def get_by_id(self, document_id: str):
=======
    async def get_one(self, document_id: str):
>>>>>>> main
        try:
            doc = await self._es.get(index=self._index, id=document_id)
        except NotFoundError:
            return None
        return self._schema(**doc['_source'])

    async def get_list(
            self,
            body,
            page_number: int = 1,
            page_size: int = 50,
    ) -> list | None:

        docs = await self._es.search(
            index=self._index,
            body=body,
            size=page_size,
            from_=((page_number - 1) * page_size)
        )

        documents = [self._schema(**doc['_source']) for doc in docs['hits']['hits']]
        return documents


def get_elastic_service(index: str, schema: Type[BaseModel]) -> ElasticAsyncSearchEngine:
    return ElasticAsyncSearchEngine(index=index, schema=schema)
