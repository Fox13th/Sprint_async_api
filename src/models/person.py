from pydantic import BaseModel

from models.film import ModelMainData


class PersonFilm(BaseModel):
    id: str
    roles: list[str]
    imdb_rating: float


class Person(ModelMainData):
    films: list[PersonFilm]
