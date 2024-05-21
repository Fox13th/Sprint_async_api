import time

from redis import Redis


if __name__ == '__main__':
    redis_conn = Redis(host='127.0.0.1', socket_connect_timeout=1)
    while True:
        if redis_conn.ping():
            break
        time.sleep(1)
