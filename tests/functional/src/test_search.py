import pytest

from functional.testdata.es_data import get_es_data


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        (
                get_es_data(),
                {'query': 'star'},
                {'status': 200, 'length': 50}
        ),
        (
                get_es_data(),
                {'query': 'Mashed potato'},
                {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(make_get_request, es_write_data, es_data: list[dict], query_data: dict, expected_answer: dict):
    await es_write_data(es_data)

    response = await make_get_request('/api/v1/films/search/', query_data)

    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
