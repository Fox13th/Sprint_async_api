import asyncio

import pytest
from fastapi.testclient import TestClient

import main
from main import app


@pytest.fixture
def client():
    client = TestClient(app)
    asyncio.run(main.startup())
    yield client


@pytest.mark.persons
def test_get_films(client):
    response = client.get('/api/v1/films')
    assert response.status_code == 200


@pytest.mark.persons
def test_get_films_search(client):
    response = client.get('/api/v1/films/search')
    assert response.status_code == 200


@pytest.mark.persons
def test_get_film(client):
    response = client.get('/api/v1/persons/2a090dde-f688-46fe-a9f4-b781a985275e')
    assert response.status_code == 200
