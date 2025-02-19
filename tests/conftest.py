import os
from typing import Any, AsyncGenerator

import pytest

from quienesquien import Client

QEQ_USER = os.environ['QEQ_USER']
QEQ_CLIENT_ID = os.environ['QEQ_CLIENT_ID']
QEQ_SECRET_ID = os.environ['QEQ_SECRET_ID']


@pytest.fixture()
async def client() -> AsyncGenerator[Client, None]:
    yield Client(QEQ_USER, QEQ_CLIENT_ID, QEQ_SECRET_ID)


@pytest.fixture(scope='session')
def vcr_config() -> dict[str, Any]:

    def filter_set_cookie_header(response):
        response['headers']['Set-Cookie'] = 'DUMMY'
        return response

    def filter_token(request):
        if request.path == '/api/token':
            return None
        return request

    config: dict[str, Any] = {
        'filter_headers': [
            ('Authorization', 'DUMMY'),
            ('cookie', None),
        ],
        'filter_query_parameters': [
            ('client_id', 'DUMMY_CLIENT_ID'),
            ('username', 'DUMMY_USERNAME'),
        ],
        'before_record_request': filter_token,
        'before_record_response': filter_set_cookie_header,
    }
    return config
