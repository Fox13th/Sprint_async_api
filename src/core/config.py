import os
from functools import lru_cache
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    project_name: str = 'movies'
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    elastic_host: str = Field('http://127.0.0.1', alias='ES_HOST')
    elastic_port: int = Field(9200, alias='ES_INTERNAL_PORT')
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logging_config.dictConfig(LOGGING)

    jwt_secret_key: str = os.environ.get('JWT_SECRET')
    jwt_algorithm: str = os.environ.get('JWT_ALGORITHM')

    debug: bool = os.environ.get('DEBUG')

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache(maxsize=None)
def get_settings(env_file: str = None):
    """Получаем настройки приложения, сохраняя в кэш."""
    return Settings(_env_file=env_file)
