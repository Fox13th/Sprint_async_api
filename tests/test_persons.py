import pytest
from fastapi.testclient import TestClient
from main import app, lifespan
import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    async with lifespan(app=app):
        with TestClient(app) as test_client:
            yield test_client


@pytest.mark.persons
def test_get_persons(client):
    response = client.get('/api/v1/persons')
    assert response.status_code == 200


@pytest.mark.persons
def test_get_persons_search(client):
    response = client.get('/api/v1/persons/search/?query=John')
    assert response.status_code == 200


@pytest.mark.persons
def test_get_person(client):
    response = client.get('/api/v1/persons/01377f6d-9767-48ce-9e37-3c81f8a3c739')
    assert response.status_code == 200


@pytest.mark.persons
def test_get_person_film(client):
    response = client.get('/api/v1/persons/01377f6d-9767-48ce-9e37-3c81f8a3c739/film/')
    assert response.status_code == 200
