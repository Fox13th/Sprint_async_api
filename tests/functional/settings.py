from pydantic import Field
from pydantic_settings import BaseSettings
from .testdata.es_mapping import settings, mappings, mappings_genre, mappings_person
import os


class TestSettings(BaseSettings):
    es_host: str = os.getenv("ELASTIC_HOST", "http://elasticsearch")
    es_index: str = 'movies'

    es_index_setting: dict = settings

    es_index_mapping: dict = mappings
    g_es_index_mapping: dict = mappings_genre
    p_es_index_mapping: dict = mappings_person

    redis_host: str = os.getenv("REDIS_HOST", "redis")
    service_url: str = os.getenv("SERVICE_URL", "http://fastapi:8000")


test_settings = TestSettings()


