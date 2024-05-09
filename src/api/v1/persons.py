from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from models.film import Person, PersonFilm
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/', response_model=list[Person])
async def persons(
        page_number: Annotated[int, Query(description='Page number', ge=1, default=1)] = 1,
        page_size: Annotated[int, Query(description='Pagination page size', ge=1, default=10)] = 10,
        person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    """Получить список всех persons."""
    persons_list = await person_service.get_list(
        page_number=page_number,
        page_size=page_size
    )
    if not persons_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return persons_list


@router.get('/search/', response_model=list[Person])
async def persons_search(
        page_number: Annotated[int, Query(description='Page number', ge=1, default=1)] = 1,
        page_size: Annotated[int, Query(description='Pagination page size', ge=1, default=10)] = 10,
        query: str = None,
        person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    """Поиск persons по запросу."""
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
    """Получить полную информацию о person."""
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return person


@router.get('/{person_id}/film/', response_model=list[PersonFilm])
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> list[PersonFilm]:
    """Получить список всех фильмов, в которых принимал участие person {person_id}."""
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return person.films



