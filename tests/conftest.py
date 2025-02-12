import os
from typing import Any, Generator

import pytest

from quienesquien import Client

QEQ_USER = os.environ['QEQ_USER']
QEQ_CLIENT_ID = os.environ['QEQ_CLIENT_ID']
QEQ_SECRET_ID = os.environ['QEQ_SECRET_ID']


@pytest.fixture(scope='module')
def client() -> Generator[Client, None, None]:
    yield Client(QEQ_USER, QEQ_CLIENT_ID, QEQ_SECRET_ID)


@pytest.fixture(scope='module')
def vcr_config() -> dict[str, Any]:

    def filter_token(request):
        if request.path == '/api/token':
            return None
        return request

    config: dict[str, Any] = dict()
    config['filter_headers'] = [
        ('Authorization', 'DUMMY'),
    ]
    config['filter_query_parameters'] = [
        ('client_id', 'DUMMY_CLIENT_ID'),
        ('username', 'DUMMY_USERNAME'),
    ]

    config['before_record_request'] = filter_token
    return config
