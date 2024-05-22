import orjson
from redis.asyncio import Redis
from redis.exceptions import ConnectionError

from src.db.backoff_decorator import backoff

redis: Redis | None = None

DATA_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class DataCache:
    def __init__(self, data_model, main_data_model=None):
        self.redis: Redis | None = redis

        self.data_model = data_model

        if main_data_model:
            self.main_data_model = main_data_model
        else:
            self.main_data_model = data_model

    @backoff((ConnectionError), 1, 2, 100, 10)
    async def _film_from_cache(self, key_cache: str):

        data = await self.redis.get(key_cache)
        if not data:
            return None

        try:
            film = self.data_model.parse_raw(data)
        except ValueError:
            film = [self.main_data_model.parse_raw(f_data) for f_data in orjson.loads(data)]

        return film

    @backoff((ConnectionError), 1, 2, 100, 10)
    async def _put_film_to_cache(self, film, key_cache: str):

        if type(film) == list:
            f_list = [f_data.json() for f_data in film]
            await self.redis.set(key_cache, orjson.dumps(f_list), DATA_CACHE_EXPIRE_IN_SECONDS)
        else:
            await self.redis.set(key_cache, film.json(), DATA_CACHE_EXPIRE_IN_SECONDS)
