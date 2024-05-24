from http import HTTPStatus

import pytest

from functional.testdata.es_data import get_es_data


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        # Вывести список кино
        (
                get_es_data('search'),
                {'id': ''},
                {'status': HTTPStatus.OK, 'length': 50, 'errors': 0}
        ),
        # Вывести конкретное кино
        (
                get_es_data('film_by_id'),
                {'id': '5ghd9bf5-0d90-4353-88ba-4ccc5d2c07ff'},
                {'status': HTTPStatus.OK, 'length': 9, 'errors': 0}
        ),
        # Тест на валидность
        (
                get_es_data('search_valid'),
                {'id': ''},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1, 'errors': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_films(make_get_request, es_write_data, valid_data, es_data: list[dict], query_data: dict,
                      expected_answer: dict):
    insert_data, errors = await valid_data(es_data, 'movies')

    await es_write_data(insert_data, 'movies')

    response = await make_get_request(f"/api/v1/films/{query_data['id']}", None)

    assert errors == expected_answer['errors']
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
