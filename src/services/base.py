from abc import ABC, abstractmethod
from typing import TypeVar
from typing import Type
from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel

from db.elastic import AsyncSearchEngine, get_elastic_service
from db.redis_db import CacheService, get_redis_service

es: AsyncElasticsearch | None = None
T = TypeVar('T', bound=BaseModel)


class BaseService(ABC):
    def __init__(
            self,
            index: str,
            schema: Type[BaseModel],
            main_data_model: Type[BaseModel] = None
    ):
        self._search_engine: AsyncSearchEngine = get_elastic_service(
            index=index,
            schema=schema
        )
        self._cache_service: CacheService = get_redis_service(
            data_model=schema,
            main_data_model=main_data_model
        )

    @abstractmethod
    async def get_by_id(self, document_id: str) -> T | None:
        pass

    @abstractmethod
    async def get_list(
            self,
            page_number: int = 1,
            page_size: int = 50,
            body: dict = None
    ) -> list[Type[T]] | None:
        pass

    async def _get_one_document(self, document_id: str, cache_key: str) -> T | None:
        document: T | None = await self._cache_service.get_from_cache(cache_key)
        if document:
            return document

        document = await self._search_engine.get_by_id(document_id=document_id)
        if not document:
            return None
        await self._cache_service.put_to_cache(document, cache_key)
        return document

    async def _get_list_documents(
            self,
            page_number: int = 1,
            page_size: int = 50,
            body: dict = None,
            cache_key: str = None
    ) -> list[T] | None:

        documents_list = await self._cache_service.get_from_cache(cache_key)
        if documents_list:
            return documents_list

        documents_list = await self._search_engine.get_list(
            body=body,
            page_number=page_number,
            page_size=page_size
        )
        if not documents_list:
            return None
        await self._cache_service.put_to_cache(documents_list, cache_key)
        return documents_list
