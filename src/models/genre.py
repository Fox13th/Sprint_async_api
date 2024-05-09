from pydantic import BaseModel

from models.film import ModelMainData


class GenreFilm(BaseModel):
    id: str
    title: str


class Genre(ModelMainData):
    description: str | None = None
    films: list[GenreFilm]
