import os
from typing import Any, AsyncGenerator

import pytest
import respx
from httpx import Response

from quienesquien import Client

QEQ_USER = os.environ['QEQ_USER']
QEQ_CLIENT_ID = os.environ['QEQ_CLIENT_ID']
QEQ_SECRET_ID = os.environ['QEQ_SECRET_ID']


@pytest.fixture()
async def client() -> AsyncGenerator[Client, None]:
    yield Client(QEQ_USER, QEQ_CLIENT_ID, QEQ_SECRET_ID)


def create_mock_response(status_code: int, message: str):
    """Helper function to create a respx mock fixture."""

    @pytest.fixture
    def _mock():
        with respx.mock(
            base_url='https://app.q-detect.com',
            assert_all_called=False,
            assert_all_mocked=False,
        ) as respx_mock:
            find_route = respx_mock.get('/api/find')
            find_route.return_value = Response(
                status_code,
                json={'success': False, 'status': message},
            )
            yield respx_mock

    return _mock


insufficient_balance_mock = create_mock_response(
    403, 'No se puede realizar la búsqueda, saldo insuficiente'
)

invalid_plan_mock = create_mock_response(
    200,
    'Tu plan de consultas ha expirado, '
    'por favor actualiza tu plan para continuar usando la API',
)

block_account_mock = create_mock_response(
    401, 'El token proporcionado para realizar esta acción es inválido'
)

internal_server_error_mock = create_mock_response(
    500, 'No se ha podido crear token'
)


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
