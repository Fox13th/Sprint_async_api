import time

from redis import Redis
from functional.settings import test_settings
import logging


if __name__ == '__main__':
    redis_conn = Redis(host=test_settings.redis_host, socket_connect_timeout=1)
    while True:
        try:
            if redis_conn.ping():
                break
            time.sleep(1)
        except Exception as e:
            _ = e
            time.sleep(1)
