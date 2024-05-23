from functools import lru_cache
from typing import Type

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel

from src.db.backoff_decorator import backoff

es: AsyncElasticsearch | None = None


class ElasticService:
    def __init__(self, index: str, schema: Type[BaseModel]):
        self._es = es
        self._index = index
        self._schema = schema

    async def get_one(self, document_id: str):
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


def get_elastic_service(index: str, schema: Type[BaseModel]) -> ElasticService:
    return ElasticService(index=index, schema=schema)