from pydantic import Field
from pydantic_settings import BaseSettings
from .testdata.es_mapping import settings, mappings, mappings_genre


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    redis_host: str = '127.0.0.1'
    es_index: str = 'movies'
    #es_id_field: str = ''
    es_index_mapping: dict = mappings
    es_index_setting: dict = settings
    g_es_index_mapping: dict = mappings_genre

    redis_host: str = '127.0.0.1'
    service_url: str = Field('http://127.0.0.1:8000')


test_settings = TestSettings()


