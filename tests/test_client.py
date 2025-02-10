import pytest


@pytest.mark.vcr
def test_search_not_found(client):
    resp = client.search('Pepito', 'Cuenca', '', 80)
    assert resp['resumen']['success'] is False
    assert resp['resumen']['num_registros'] == 0
    assert resp['persons'] == []


@pytest.mark.vcr
def test_search(client):
    resp = client.search('Andres Manuel', 'Lopez', 'Obrador', 80)
    assert resp['resumen']['success'] is True
    assert resp['resumen']['num_registros'] != 0
    assert resp['persons'] is not None


@pytest.mark.vcr
def test_search_with_params(client):
    resp = client.search(
        nombre='Andres Manuel',
        paterno='Lopez',
        materno='Obrador',
        match_score=85,
        rfc='LOOA531113F15',
        curp='LOOA531113HTCPBN07',
        sex='M',
        birthday='13/11/1953',
        search_type=0,
        search_list='PPE',
    )
    assert resp['resumen']['success'] is True
    assert resp['resumen']['num_registros'] != 0
    assert resp['persons'] is not None
