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
    imdb_rating: float = None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(FilmMainData):
    description: str = None  # Жду ETL
    # genres: List[GenreMainData]
    directors: List[Person] = None  # Жду ETL
    actors: List[Person] = None  # Жду ETL
    writers: List[Person] = None  # Жду ETL
    # created_at: datetime
