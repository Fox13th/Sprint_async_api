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


@pytest.mark.genres
def test_get_genres(client):
    response = client.get('/api/v1/genres')
    assert response.status_code == 200


@pytest.mark.genres
def test_get_genre(client):
    response = client.get('/api/v1/genres/3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff')
    assert response.status_code == 200
