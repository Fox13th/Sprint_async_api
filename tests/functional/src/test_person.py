from http import HTTPStatus

import pytest

from functional.testdata.es_data import get_es_data


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        # Вывести список персон
        (
                get_es_data('list_persons'),
                {'id': ''},
                {'status': HTTPStatus.OK, 'length': 10, 'errors': 0}
        ),
        # Вывести конкретную персону
        (
                get_es_data('person_by_id'),
                {'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'},
                {'status': HTTPStatus.OK, 'length': 3, 'errors': 0}
        ),
        # Тест на валидность
        (
                get_es_data('persons_valid'),
                {'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1, 'errors': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_person(
        make_get_request,
        es_write_data,
        valid_data,
        es_data: list[dict],
        query_data: dict,
        expected_answer: dict
):
    insert_data, errors = await valid_data(es_data, 'persons')

    await es_write_data(insert_data, 'persons')

    response = await make_get_request(f"/api/v1/persons/{query_data['id']}", None)

    assert errors == expected_answer['errors']
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
