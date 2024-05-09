from datetime import datetime

import orjson

from models.common import BaseOrjsonModel
from models.genre import GenreBaseData
from models.person import PersonBaseData


class FilmMainData(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float = None


class Film(FilmMainData):
    description: str | None
    genres: list[GenreBaseData]
    directors: list[PersonBaseData]
    actors: list[PersonBaseData]
    writers: list[PersonBaseData]
    creation_date: datetime | None = None
