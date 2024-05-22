from aiohttp.client_exceptions import ClientConnectorError
from elasticsearch import AsyncElasticsearch, exceptions

from src.db.backoff_decorator import backoff

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    return es
