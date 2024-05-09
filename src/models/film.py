from datetime import datetime

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class GenreFilm(BaseModel):
    id: str
    title: str


class GenreMainData(BaseOrjsonModel):
    id: str
    name: str


class Genre(GenreMainData):
    description: str | None = None
    films: list[GenreFilm]


class PersonFilm(BaseModel):
    id: str
    roles: list[str]
    imdb_rating: float


class PersonMainData(BaseOrjsonModel):
    id: str
    name: str


class Person(PersonMainData):
    films: list[PersonFilm]


class FilmMainData(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float = None


class Film(FilmMainData):
    description: str
    genres: list[GenreMainData]
    directors: list[PersonMainData]
    actors: list[PersonMainData]
    writers: list[PersonMainData]
    creation_date: datetime | None = None
