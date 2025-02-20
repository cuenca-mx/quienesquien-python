import datetime as dt

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
async def test_reusable_token(client: Client) -> None:
    resp1 = await client.search('Andres Manuel Lopez Obrador', 80)
    resp2 = await client.search('Marcelo Luis Ebrard Casaubón', 80)
    assert len(resp1) != 0
    assert len(resp2) != 0


@pytest.mark.vcr
async def test_invalid_token(client: Client, respx_mock):
    respx_mock.get('https://app.q-detect.com/api/token').mock(
        return_value=Response(200, text='an_invalid_token')
    )
    respx_mock.get('https://app.q-detect.com/api/find').pass_through()
    with pytest.raises(InvalidTokenError):
        await client.search('Pepito Cuenca', 80)
    assert client._auth_token is None


@pytest.mark.vcr
async def test_invalid_plan(client: Client, respx_mock) -> None:
    respx_mock.get('https://app.q-detect.com/api/token').pass_through()
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
    respx_mock.get('https://app.q-detect.com/api/token').pass_through()
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
    respx_mock.get('https://app.q-detect.com/api/token').pass_through()
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
    respx_mock.get('https://app.q-detect.com/api/token').pass_through()
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
    respx_mock.get('https://app.q-detect.com/api/token').pass_through()
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
async def test_token_error_response(client: Client, respx_mock) -> None:
    respx_mock.get('https://app.q-detect.com/api/token').mock(
        return_value=Response(
            500,
            json={
                'success': False,
                'status': 'No se ha podido crear token',
            },
        )
    )
    respx_mock.get('https://app.q-detect.com/api/find').pass_through()
    with pytest.raises(QuienEsQuienError):
        await client.search('Pepito Cuenca', 80)


async def test_invalid_search_criteria(client: Client) -> None:
    with pytest.raises(InvalidSearchCriteriaError):
        await client.search(
            match_score=85,
            gender=Gender.masculino,
            birthday=dt.date(1953, 11, 13),
            search_type=SearchType.fisica,
            search_list=(SearchList.PPE, SearchList.ONU),
        )
