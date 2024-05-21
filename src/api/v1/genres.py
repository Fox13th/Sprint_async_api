from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from services.genres import GenreService, get_genre_service
from models.genre import Genre

router = APIRouter()


@router.get('/', response_model=list[Genre])
async def list_genres(
        page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 50,
        page_number: Annotated[int, Query(description='Page number', ge=1)] = 1,
        genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    """
    Вывод списка жанров
    Пример запроса: http://127.0.0.1:8000/api/v1/genres
    :param genre_service:
    :param page_size: Количество элементов на странице
    :param page_number: Номер страницы
    """

    genres = await genre_service.get_genre(None, page_size, page_number)

    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre(s) not found')

    genres: list[Genre] = sorted(genres, key=lambda x: x.name)

    return genres


# Получить жанр по id
@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    """
    Вывод жанра по id.
    Пример запроса: http://127.0.0.1:8000/api/v1/genres/5373d043-3f41-4ea8-9947-4b746c601bbd
    :param genre_service:
    :param genre_id: id кинофильма
    """

    genre = await genre_service.get_genre(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return genre
