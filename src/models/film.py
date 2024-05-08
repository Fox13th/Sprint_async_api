from datetime import datetime

import orjson
from pydantic import BaseModel

from models.genre import GenreMainData
from models.person import PersonMainData


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FilmMainData(BaseModel):
    id: str
    title: str
    imdb_rating: float = None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(FilmMainData):
    description: str
    genres: list[GenreMainData]
    directors: list[PersonMainData]
    actors: list[PersonMainData]
    writers: list[PersonMainData]
    creation_date: datetime | None = None
      