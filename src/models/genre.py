from pydantic import BaseModel
from models.common import BaseOrjsonModel


class GenreFilm(BaseModel):
    id: str
    title: str


class GenreBaseData(BaseOrjsonModel):
    id: str
    name: str


class Genre(GenreBaseData):
    description: str | None = None
    films: list[GenreFilm]
