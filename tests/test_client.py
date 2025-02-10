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
