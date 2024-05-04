from enum import Enum
from datetime import datetime
from typing import List

import orjson
from pydantic import BaseModel

from models.film import FilmMainData


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class PersonRole(Enum):
    director = 'director'
    actor = 'actor'
    writer = 'writer'


class PersonFilm(BaseModel):
    id: str
    title: str
    roles: List[PersonRole]


class Person(BaseModel):
    id: str
    full_name: str
    films: List[PersonFilm]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# class Person(PersonMainData):
#     films: List[PersonFilmData]
