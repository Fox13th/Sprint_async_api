import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv

from functional.utils.backoff_decorator import backoff


@backoff((ConnectionError, requests.exceptions.ConnectionError), 1, 2, 100)
def es_ping():
    res = requests.get(f"http://{os.getenv('ES_HOST')}:{os.getenv('ES_INTERNAL_PORT')}/_cluster/health")
    if res.status_code == HTTPStatus.OK:
        return


if __name__ == '__main__':
    load_dotenv()
    es_ping()
W