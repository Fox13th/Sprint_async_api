import asyncio
import uuid
from asyncio import sleep

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from elasticsearch.helpers import async_bulk

from .settings import test_settings

from .models.film import Film
from .models.genre import Genre


@pytest_asyncio.fixture(name='valid_data')
def valid_data():
    async def inner(es_data: list[dict], model_idx):
        bulk_query: list[dict] = []
        count_err = 0
        for row in es_data:
            try:
                if model_idx == 'genres':
                    Genre(**row)
                else:
                    Film(**row)
                data = {'_index': model_idx, '_id': row['id']}
                data.update({'_source': row})
                bulk_query.append(data)
            except ValueError as err:
                i_err = str(err).split(' ')
                count_err = int(i_err[0])
        return bulk_query, count_err

    return inner


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='es_data')
async def es_data():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client):
    async def inner(es_data: list[dict], es_index):

        if await es_client.indices.exists(index=es_index):
            await es_client.indices.delete(index=es_index)

        if es_index == 'movies':
            mapping = test_settings.es_index_mapping
        else:
            mapping = test_settings.g_es_index_mapping

        print(es_index)

        res = await es_client.indices.create(index=es_index,
                                       settings=test_settings.es_index_setting,
                                       mappings=mapping)
        print(res)

        updated, errors = await async_bulk(client=es_client, actions=es_data)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

        await sleep(1)

    return inner


@pytest_asyncio.fixture(name='cl_session', scope='session')
async def cl_session():
    cl_session = aiohttp.ClientSession()
    yield cl_session
    await cl_session.close()


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(cl_session):
    async def inner(api_service, query_data):
        url = test_settings.service_url + api_service
        async with cl_session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            print(str(status))
        res = {'status': status, 'body': body}
        return res

    return inner
