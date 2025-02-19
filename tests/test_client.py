import datetime as dt

import pytest

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
async def test_invalid_token(client: Client, mocker) -> None:
    mock_response = mocker.Mock()
    mock_response.text = 'invalid_token'
    mocker.patch.object(
        client, '_fetch_auth_token', return_value=mock_response
    )
    with pytest.raises(InvalidTokenError):
        await client.search('Pepito Cuenca', 80)
    assert client._auth_token is None


async def test_invalid_plan(client: Client, invalid_plan_mock) -> None:
    with pytest.raises(InvalidPlanError):
        await client.search('Pepito Cuenca', 80)


async def test_insufficient_balance(
    client: Client, insufficient_balance_mock
) -> None:
    with pytest.raises(InsufficientBalanceError):
        await client.search('Pepito Cuenca', 80)


async def test_block_account(client: Client, block_account_mock) -> None:
    with pytest.raises(InvalidTokenError):
        await client.search('Pepito Cuenca', 80)


async def test_internal_server_error(
    client: Client, internal_server_error_mock
) -> None:
    with pytest.raises(QuienEsQuienError):
        await client.search('Pepito Cuenca', 80)


async def test_http_error(client: Client, mocker) -> None:
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        'success': False,
        'status': '“No se ha podido crear token',
    }
    mocker.patch.object(client, '_make_request', return_value=mock_response)

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
