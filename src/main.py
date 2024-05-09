import logging

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from contextlib import asynccontextmanager


from api.v1 import films, genres, persons

from core import config
from core.logger import LOGGING
from db import elastic, redis_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """@app.on_event("startup") and @app.on_event("shutdown") was deprecated.\n
    Recommended to use "lifespan"."""
    # startup
    redis_db.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
    yield

    # shutdown
    await redis_db.redis.close()
    await elastic.es.close()


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])

app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])

app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
