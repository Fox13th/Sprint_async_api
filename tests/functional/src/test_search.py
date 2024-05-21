import pytest

from functional.testdata.es_data import get_es_data


@pytest.mark.parametrize(
    'mode_search, es_data, query_data, expected_answer',
    [
        (
                'films',
                get_es_data('search'),
                {'query': 'star'},
                {'status': 200, 'length': 50, 'errors': 0}
        ),
        (
                'films',
                get_es_data('search'),
                {'query': 'Mashed potato'},
                {'status': 404, 'length': 1, 'errors': 0}
        ),
        (
                'films',
                get_es_data('search_valid'),
                {'query': 'star'},
                {'status': 404, 'length': 1, 'errors': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(make_get_request, es_write_data, valid_data, mode_search, es_data: list[dict], query_data: dict,
                      expected_answer: dict):
    insert_data, errors = await valid_data(es_data, 'movies')

    await es_write_data(insert_data, 'movies')

    response = await make_get_request(f'/api/v1/{mode_search}/search/', query_data)

    assert errors == expected_answer['errors']
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
