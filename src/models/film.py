from datetime import datetime

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ModelMainData(BaseOrjsonModel):
    id: str
    name: str


class FilmMainData(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float = None


class Film(FilmMainData):
    description: str | None
    genres: list[ModelMainData]
    directors: list[ModelMainData]
    actors: list[ModelMainData]
    writers: list[ModelMainData]
    creation_date: datetime | None = None
