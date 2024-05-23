import pytest

from functional.testdata.es_data import get_es_data


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        # Вывести список жанров
        (
                get_es_data('list_genres'),
                {'id': ''},
                {'status': 200, 'length': 10, 'errors': 0}
        ),
        # Вывести конкретный жанр
        (
                get_es_data('genres_by_id'),
                {'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'},
                {'status': 200, 'length': 4, 'errors': 0}
        ),
        # Тест на валидность
        (
                get_es_data('genres_valid'),
                {'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'},
                {'status': 404, 'length': 1, 'errors': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_genre(make_get_request, es_write_data, valid_data, es_data: list[dict], query_data: dict,
                      expected_answer: dict):
    insert_data, errors = await valid_data(es_data, 'genres')

    await es_write_data(insert_data, 'genres')

    response = await make_get_request(f"/api/v1/genres/{query_data['id']}", None)

    assert errors == expected_answer['errors']
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
