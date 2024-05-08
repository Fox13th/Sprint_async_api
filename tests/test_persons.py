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
