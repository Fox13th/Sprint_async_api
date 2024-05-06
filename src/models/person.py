from enum import Enum
from typing import List

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class PersonFilm(BaseModel):
    id: str
    roles: List[str]


class Person(BaseModel):
    id: str
    name: str
    films: List[PersonFilm]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
