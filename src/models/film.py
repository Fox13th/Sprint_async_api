from datetime import datetime
from typing import List, Optional

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
    genres: List[GenreMainData]
    directors: List[PersonMainData]
    actors: List[PersonMainData]
    writers: List[PersonMainData]
    creation_date: Optional[datetime] = None
