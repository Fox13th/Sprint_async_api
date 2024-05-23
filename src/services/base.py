from db.elastic import get_elastic_service
from db.redis_db import get_redis_service

from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseService:

    def __init__(
            self,
            index: str,
            schema: Type[BaseModel],
            main_data_model: Type[BaseModel] = None,
    ):
        self._redis_service = get_redis_service(data_model=schema, main_data_model=main_data_model)
        self._elastic_service = get_elastic_service(index=index, schema=schema)

    async def _get_one_document(self, document_id: str, cache_key: str) -> T | None:
        document = await self._redis_service.get_from_cache(cache_key)
        if document:
            return document

        document = await self._elastic_service.get_one(document_id=document_id)
        if not document:
            return None
        await self._redis_service.put_to_cache(document, cache_key)
        return document

    async def _get_list_documents(
            self,
            page_number: int = 1,
            page_size: int = 50,
            body: dict = None,
            cache_key: str = None
    ) -> list[Type[T]] | None:

        documents_list = await self._redis_service.get_from_cache(cache_key)
        if documents_list:
            return documents_list

        documents_list = await self._elastic_service.get_list(body=body, page_number=page_number, page_size=page_size)
        if not documents_list:
            return None
        await self._redis_service.put_to_cache(documents_list, cache_key)
        return documents_list
