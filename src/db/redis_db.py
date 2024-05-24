from abc import ABC, abstractmethod
from typing import Type, TypeVar

import orjson
from pydantic import BaseModel
from redis.asyncio import Redis
from redis.exceptions import ConnectionError

from db.backoff_decorator import backoff

redis: Redis | None = None
DATA_CACHE_EXPIRE_IN_SECONDS = 60 * 5
T = TypeVar('T', bound=BaseModel)


class CacheService(ABC):
    @abstractmethod
    async def get_from_cache(self, key_cache: str) -> T | list[T] | None:
        pass

    @abstractmethod
    async def put_to_cache(self, data, key_cache: str) -> None:
        pass


class RedisCacheService(CacheService):
    def __init__(self, data_model, main_data_model=None):
        self.redis: Redis | None = redis

        self.data_model = data_model

        if main_data_model:
            self.main_data_model = main_data_model
        else:
            self.main_data_model = data_model

    @backoff((ConnectionError,), 1, 2, 100, 10)
    async def get_from_cache(self, key_cache: str):

        data = await self.redis.get(key_cache)
        if not data:
            return None

        try:
            film = self.data_model.parse_raw(data)
        except ValueError:
            film = [self.main_data_model.parse_raw(f_data) for f_data in orjson.loads(data)]

        return film

    @backoff((ConnectionError,), 1, 2, 100, 10)
    async def put_to_cache(self, data, key_cache: str):

        if isinstance(data, list):
            f_list = [f_data.json() for f_data in data]
            await self.redis.set(key_cache, orjson.dumps(f_list), DATA_CACHE_EXPIRE_IN_SECONDS)
        else:
            await self.redis.set(key_cache, data.json(), DATA_CACHE_EXPIRE_IN_SECONDS)


def get_redis_service(
        data_model: Type[BaseModel],
        main_data_model: Type[BaseModel] = None
):
    redis_service = RedisCacheService(
        data_model=data_model,
        main_data_model=main_data_model
    )
    return redis_service
