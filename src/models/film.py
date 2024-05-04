from datetime import datetime
from typing import List

import orjson
from pydantic import BaseModel

from models.genre import GenreMainData
from models.person import Person


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FilmMainData(BaseModel):
    id: str
    title: str
    imdb_rating: float

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(FilmMainData):
    description: str
    genres: List[GenreMainData]
    directors: List[Person]
    actors: List[Person]
    writers: List[Person]
    created_at: datetime
