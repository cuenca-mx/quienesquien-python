import os
from typing import Any, AsyncGenerator

import pytest

from quienesquien import Client

QEQ_USER = os.environ['QEQ_USER']
QEQ_AUTH_TOKEN = os.environ['QEQ_AUTH_TOKEN']


@pytest.fixture()
async def client() -> AsyncGenerator[Client, None]:
    yield Client(QEQ_USER, QEQ_AUTH_TOKEN)


@pytest.fixture(scope='session')
def vcr_config() -> dict[str, Any]:

    def filter_sensitive_data(response):
        response['headers']['Set-Cookie'] = 'DUMMY_SET_COOKIE'
        if response['headers']['Content-Type'] == ['text/html; charset=UTF-8']:
            response['body'] = {'string': b'DUMMY_RESPONSE_TOKEN'}
        return response

    config: dict[str, Any] = {
        'filter_headers': [
            ('Authorization', 'DUMMY_AUTHORIZATION'),
            ('cookie', None),
        ],
        'filter_query_parameters': [
            ('client_id', 'DUMMY_CLIENT_ID'),
            ('username', 'DUMMY_USERNAME'),
        ],
        'before_record_response': filter_sensitive_data,
    }
    return config
