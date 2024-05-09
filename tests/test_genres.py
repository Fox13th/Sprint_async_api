import pytest
from fastapi.testclient import TestClient
from main import app, lifespan
import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    async with lifespan(app=app):
        with TestClient(app) as test_client:
            yield test_client


@pytest.mark.genres
def test_get_genres(client):
    response = client.get('/api/v1/genres')
    assert response.status_code == 200


@pytest.mark.genres
def test_get_genre(client):
    response = client.get('/api/v1/genres/3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff')
    assert response.status_code == 200
