import redis
from redis import Redis

from tests.functional.settings import test_settings

from tests.functional.utils.backoff_decorator import backoff


@backoff((redis.exceptions.ConnectionError, ), 1, 2, 100)
def redis_ping():
    redis_conn = Redis(host=test_settings.redis_host, socket_connect_timeout=1)
    redis_conn.ping()


if __name__ == '__main__':
    redis_ping()
