from typing import Annotated
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from models.film import Film, FilmMainData
from services.auth import security_jwt
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/',
            response_model=list[FilmMainData],
            summary='Вывод всех кинопроизведений по рейтингу',
            description='Получение списка кинопроизведений согласно их рейтингу',
            response_description="Название и рейтинг фильма",
            tags=['Общий вывод']
            )
async def popular_films(
        user: Annotated[dict, Depends(security_jwt(required_roles=['superuser']))],
        sort: str | None = '-imdb_rating',
        genre: str | None = None,
        page_size: Annotated[int, Query(description='Количество элементов на странице', ge=1)] = 50,
        page_number: Annotated[int, Query(description='Номер страницы', ge=1)] = 1,
        film_service: FilmService = Depends(get_film_service)
) -> list[FilmMainData]:
    """
    Вывод популярных фильмов.
    Пример запроса: http://127.0.0.1:8000/api/v1/films?sort=-imdb_rating&page_number=1&page_size=50
                    http://127.0.0.1:8000/api/v1/films?sort=-imdb_rating&genre=5373d043-3f41-4ea8-9947-4b746c601bbd
    :param user:
    :param film_service:
    :param genre: Фильтрация по жанру
    :param page_size: Количество элементов на странице
    :param page_number: Номер страницы
    :param sort: По какому полю сортировать; по умолчанию: '-imdb_rating'
    """
    print(user['sub'])
    print(user['sub']['user_id'])

    films = await film_service.get_list(
        page_number=page_number,
        page_size=page_size,
        sort_by=sort,
        genre=genre
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film(s) not found')
    return films


@router.get('/search/',
            response_model=list[FilmMainData],
            summary='Поиск по фильмам',
            description='Осуществляется поиск кино по его названию',
            response_description="Название и рейтинг фильма",
            tags=['Полнотекстовой поиск']
            )
async def search_films(
        query: str,
        page_size: Annotated[int, Query(description='Количество элементов на странице', ge=1)] = 50,
        page_number: Annotated[int, Query(description='Номер страницы', ge=1)] = 1,
        film_service: FilmService = Depends(get_film_service)
) -> list[FilmMainData]:
    """
    Поиск по фильмам.
    Пример запроса: http://127.0.0.1:8000/api/v1/films/search/?query=star&page_number=1&page_size=50
    :param query: Поисковое слово
    :param page_size: количество найденных фильмов на странице
    :param page_number: номер страницы
    """

    films = await film_service.get_list(
        query=query,
        page_size=page_size,
        page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film(s) not found')

    return films


# Получить кино по id
@router.get('/{film_id}',
            response_model=Film,
            summary='Поиск конкретного кинопроизведения',
            description='Осуществляется поиск кино по его уникальному идентификатору',
            response_description="Название, рейтинг, описание, жанр, съемочная команда фильма",
            tags=['Поиск по id']
            )
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    """
    Вывод кино по id.
    Пример запроса: http://127.0.0.1:8000/api/v1/films/833b1926-ef16-49a1-b41d-eddd618a036e
                    http://127.0.0.1:8000/api/v1/films/4e5184c8-54eb-4f09-be83-4f95affe42a8
    :param film_id: id кинофильма
    """
    film = await film_service.get_by_id(film_id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return film
