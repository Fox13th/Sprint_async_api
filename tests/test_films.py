import pytest
from fastapi.testclient import TestClient
from main import app, lifespan
import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    async with lifespan(app=app):
        with TestClient(app) as test_client:
            yield test_client


@pytest.mark.films
def test_get_films(client):
    response = client.get('/api/v1/films')
    assert response.status_code == 200


@pytest.mark.films
def test_get_films_search(client):
    response = client.get('/api/v1/films/search/?query=test')
    assert response.status_code == 200


@pytest.mark.films
def test_get_film(client):
    response = client.get('/api/v1/films/2a090dde-f688-46fe-a9f4-b781a985275e')
    assert response.status_code == 200
