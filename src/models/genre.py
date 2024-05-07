from typing import List

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class GenreFilm(BaseModel):
    id: str
    title: str


class GenreMainData(BaseModel):
    id: str
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genre(GenreMainData):
    description: str = None
    films: List[GenreFilm]
