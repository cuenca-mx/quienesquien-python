import datetime as dt

import pytest

from quienesquien import Client
from quienesquien.enums import Gender, SearchList, SearchType


@pytest.mark.vcr
async def test_search_not_found(client: Client) -> None:
    resp = await client.search('Pepito', 'Cuenca', '', 80)
    assert resp.success is False
    assert resp.num_registros == 0
    assert resp.persons == []


@pytest.mark.vcr
async def test_search(client: Client) -> None:
    resp = await client.search('Andres Manuel', 'Lopez', 'Obrador', 80)
    assert resp.success is True
    assert resp.num_registros != 0
    assert resp.persons is not None


@pytest.mark.vcr
async def test_search_with_params(client: Client) -> None:
    resp = await client.search(
        nombre='Andres Manuel',
        paterno='Lopez',
        materno='Obrador',
        match_score=85,
        rfc='LOOA531113F15',
        curp='LOOA531113HTCPBN07',
        gender=Gender.masculino,
        birthday=dt.date(1953, 11, 13),
        search_type=SearchType.fisica,
        search_list=(SearchList.PPE, SearchList.ONU),
    )
    assert resp.success is True
    assert resp.num_registros != 0
    assert resp.persons is not None
