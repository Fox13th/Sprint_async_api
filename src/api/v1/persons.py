from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models.person import Person, PersonFilm
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/', response_model=List[Person])
async def persons(
        page_number: int = 1,
        page_size: int = 10,
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:
    """Получить список всех persons."""
    persons_list = await person_service.get_list(
        page_number=page_number,
        page_size=page_size
    )
    if not persons_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return persons_list


@router.get('/search/', response_model=List[Person])
async def persons_search(
        page_number: int = 1,
        page_size: int = 10,
        query: str = None,
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:
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


@router.get('/{person_id}/film/', response_model=List[PersonFilm])
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> List[PersonFilm]:
    """Получить список всех фильмов, в которых принимал участие person {person_id}."""
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return person.films



