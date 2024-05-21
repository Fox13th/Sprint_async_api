from pydantic import BaseModel

from .common import BaseOrjsonModel


class PersonFilm(BaseModel):
    id: str
    roles: list[str]
    imdb_rating: float


class PersonBaseData(BaseOrjsonModel):
    id: str
    name: str


class Person(PersonBaseData):
    films: list[PersonFilm]
