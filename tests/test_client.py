import datetime as dt
import os

import pytest
from httpx import Response

from quienesquien import Client
from quienesquien.enums import Gender, SearchList, SearchType
from quienesquien.exc import (
    InsufficientBalanceError,
    InvalidPlanError,
    InvalidSearchCriteriaError,
    InvalidTokenError,
    PersonNotFoundError,
    QuienEsQuienError,
)

QEQ_SECRET_ID = os.environ['QEQ_SECRET_ID']
QEQ_CLIENT_ID = os.environ['QEQ_CLIENT_ID']
QEQ_USER = os.environ['QEQ_USER']


@pytest.mark.vcr
async def test_search_not_found(client: Client) -> None:
    with pytest.raises(PersonNotFoundError):
        await client.search('Pepito Cuenca ', 80)


@pytest.mark.vcr
async def test_search_by_name(client: Client) -> None:
    resp = await client.search('Andres Manuel Lopez Obrador', 80)
    assert len(resp) != 0


@pytest.mark.vcr
async def test_search_by_curp(client: Client) -> None:
    resp = await client.search(
        match_score=85,
        curp='LOOA531113HTCPBN07',
        gender=Gender.masculino,
        birthday=dt.date(1953, 11, 13),
        search_type=SearchType.fisica,
        search_list=(SearchList.PPE, SearchList.ONU),
    )
    assert len(resp) != 0


@pytest.mark.vcr
async def test_search_with_params(client: Client) -> None:
    resp = await client.search(
        full_name='Andres Manuel Lopez Obrador',
        match_score=85,
        rfc='LOOA531113F15',
        curp='LOOA531113HTCPBN07',
        gender=Gender.masculino,
        birthday=dt.date(1953, 11, 13),
        search_type=SearchType.fisica,
        search_list=(SearchList.PPE, SearchList.ONU),
    )
    assert len(resp) != 0


@pytest.mark.vcr
async def test_invalid_token(client: Client):
    client.auth_token = 'an_invalid_token'
    with pytest.raises(InvalidTokenError):
        await client.search('Pepito Cuenca', 80)


@pytest.mark.vcr
async def test_invalid_plan(client: Client, respx_mock) -> None:
    respx_mock.get('https://app.q-detect.com/api/find').mock(
        return_value=Response(
            200,
            json={
                'success': False,
                'status': 'Tu plan de consultas ha expirado, '
                'por favor actualiza tu plan para continuar usando la API',
            },
        )
    )
    with pytest.raises(InvalidPlanError):
        await client.search('Pepito Cuenca', 80)


@pytest.mark.vcr
async def test_insufficient_balance(client: Client, respx_mock) -> None:
    respx_mock.get('https://app.q-detect.com/api/find').mock(
        return_value=Response(
            403,
            json={
                'success': False,
                'status': 'No se puede realizar la búsqueda, '
                'saldo insuficiente',
            },
        )
    )
    with pytest.raises(InsufficientBalanceError):
        await client.search('Pepito Cuenca', 80)


@pytest.mark.vcr
async def test_block_account(client: Client, respx_mock) -> None:
    respx_mock.get('https://app.q-detect.com/api/find').mock(
        return_value=Response(
            401,
            json={
                'success': False,
                'status': (
                    'El token proporcionado para realizar '
                    'esta acción es inválido'
                ),
            },
        )
    )
    with pytest.raises(InvalidTokenError):
        await client.search('Pepito Cuenca', 80)


@pytest.mark.vcr
async def test_internal_server_error(client: Client, respx_mock) -> None:
    respx_mock.get('https://app.q-detect.com/api/find').mock(
        return_value=Response(
            500,
            json={
                'success': False,
                'status': 'Internal server error',
            },
        )
    )
    with pytest.raises(QuienEsQuienError):
        await client.search('Pepito Cuenca', 80)


@pytest.mark.vcr
async def test_unknown_error(client: Client, respx_mock) -> None:
    respx_mock.get('https://app.q-detect.com/api/find').mock(
        return_value=Response(
            200,
            json={
                'success': False,
                'status': 'Unknown error',
            },
        )
    )
    with pytest.raises(QuienEsQuienError):
        await client.search('Pepito Cuenca', 80)


@pytest.mark.vcr
async def test_create_token() -> None:
    token = await Client.create_token(QEQ_CLIENT_ID, QEQ_SECRET_ID)
    client = Client(QEQ_USER, token)
    resp = await client.search('Andres Manuel Lopez Obrador', 80)
    assert len(resp) != 0


@pytest.mark.vcr
async def test_token_error_response(respx_mock) -> None:
    respx_mock.get('https://app.q-detect.com/api/token').mock(
        return_value=Response(
            500,
            json={
                'success': False,
                'status': 'No se ha podido crear token',
            },
        )
    )
    with pytest.raises(QuienEsQuienError):
        await Client.create_token(QEQ_CLIENT_ID, QEQ_SECRET_ID)


async def test_invalid_search_criteria(client: Client) -> None:
    with pytest.raises(InvalidSearchCriteriaError):
        await client.search(
            match_score=85,
            gender=Gender.masculino,
            birthday=dt.date(1953, 11, 13),
            search_type=SearchType.fisica,
            search_list=(SearchList.PPE, SearchList.ONU),
        )


async def test_client_without_token() -> None:
    search_client = Client('my_username')
    with pytest.raises(AssertionError) as excinfo:
        await search_client.search('Andres Manuel Lopez Obrador', 80)
    assert (
        str(excinfo.value)
        == 'you must create or reuse an already created auth token'
    )
