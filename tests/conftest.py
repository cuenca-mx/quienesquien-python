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


def mask_first_response(
    response: dict[str, Any], interaction_count: int
) -> dict[str, Any]:
    """Mask the first response to avoid exposing the response token"""
    if interaction_count == 0 and response['body']['string']:
        response['body']['string'] = b'DUMMY'
    return response


@pytest.fixture(scope='module')
def vcr_config() -> dict[str, Any]:
    request_counter = 0

    def before_record_response(response: dict[str, Any]) -> dict[str, Any]:
        nonlocal request_counter
        response = mask_first_response(response, request_counter)
        request_counter += 1
        return response

    config: dict[str, Any] = dict()
    config['filter_headers'] = [
        ('Authorization', 'DUMMY'),
    ]
    config['filter_query_parameters'] = [
        ('client_id', 'DUMMY_CLIENT_ID'),
        ('username', 'DUMMY_USERNAME'),
    ]

    config['before_record_response'] = before_record_response
    return config


@pytest.fixture(autouse=True, scope='function')
def reset_request_counter(vcr_config: dict[str, Any]) -> None:
    """Reset the request counter in each test"""
    vcr_config['before_record_response'].__closure__[0].cell_contents = 0
