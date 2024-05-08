from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from services.genres import GenreService, get_genre_service
from models.genre import Genre, GenreMainData

router = APIRouter()


@router.get('/', response_model=List[Genre])
async def list_genres(page_size: int = Query(50, gt=0), page_number: int = Query(1, gt=0),
                      genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    """
    Вывод списка жанров
    Пример запроса: http://127.0.0.1:8000/api/v1/genres
    :param page_size: Количество элементов на странице
    :param page_number: Номер страницы
    """

    genres = await genre_service.get_genre(None, page_size, page_number)

    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre(s) not found')

    genres = sorted(genres, key=lambda x: x.name)

    return genres


# Получить жанр по id
@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    """
    Вывод жанра по id.
    Пример запроса: http://127.0.0.1:8000/api/v1/genres/5373d043-3f41-4ea8-9947-4b746c601bbd
    :param genre_id: id кинофильма
    """

    genre = await genre_service.get_genre(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return Genre(id=genre.id, name=genre.name, title=genre.description, films=genre.films)
