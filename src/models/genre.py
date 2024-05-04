from typing import List

import orjson
from pydantic import BaseModel

from models.film import FilmMainData


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
    description: str
    films: List[GenreFilm]
