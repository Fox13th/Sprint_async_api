from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models.person import Person
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(id=person.id, title=person.name)


@router.get('/', response_model=List[Person])
async def persons(
        page_number: int = 1,
        page_size: int = 10,
        query: str = None,
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:
    persons_list = await person_service.get_list(
        page_number=page_number,
        page_size=page_size,
        query=query
    )
    if not persons_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return persons_list
