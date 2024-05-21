from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from models.person import Person, PersonFilm
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/', response_model=list[Person])
async def persons(
        page_number: Annotated[int, Query(description='Page number', ge=1)] = 1,
        page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
        person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    """
    Вывод списка персон
    Пример запроса: http://127.0.0.1:8000/api/v1/persons/
    :param person_service:
    :param page_size: Количество элементов на странице
    :param page_number: Номер страницы
    """

    persons_list = await person_service.get_list(
        page_number=page_number,
        page_size=page_size
    )
    if not persons_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return persons_list


@router.get('/search/', response_model=list[Person])
async def persons_search(
        page_number: Annotated[int, Query(description='Page number', ge=1)] = 1,
        page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
        query: str = None,
        person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    """
    Поиск персон по запросу.
    Поиск по фильмам.
    Пример запроса: http://127.0.0.1:8000/api/v1/persons/search/?query=jhon&page_number=1&page_size=50
    :param person_service:
    :param query: Поисковое слово
    :param page_size: количество найденных фильмов на странице
    :param page_number: номер страницы
    """

    persons_list = await person_service.get_list(
        page_number=page_number,
        page_size=page_size,
        query=query
    )
    if not persons_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return persons_list


@router.get('/{person_id}', response_model=Person)
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> Person:
    """
    Вывод полной информации о персоне по person_id.
    Пример запроса: http://127.0.0.1:8000/api/v1/persons/833b1926-ef16-49a1-b41d-eddd618a036e
                    http://127.0.0.1:8000/api/v1/persons/4e5184c8-54eb-4f09-be83-4f95affe42a8
    :param person_service:
    :param person_id: id персоны"""

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return person


@router.get('/{person_id}/film/', response_model=list[PersonFilm])
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> list[PersonFilm]:
    """
    Получить список всех фильмов, в которых принимал участие person {person_id}.
    Пример запроса: http://127.0.0.1:8000/api/v1/persons/833b1926-ef16-49a1-b41d-eddd618a036e/film/
                    http://127.0.0.1:8000/api/v1/persons/4e5184c8-54eb-4f09-be83-4f95affe42a8/film/
    :param person_service:
    :param person_id: id персоны
    """

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return person.films
