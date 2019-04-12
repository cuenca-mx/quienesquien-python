import vcr

from quienesquien.client import Client


USER = 'pepito@cuenca.com'
PASSWORD = 'notsecurepassword'
URL = 'https://peps.mx/datos/qws'


@vcr.use_cassette()
def test_search_not_found():

    client = Client(URL, USER, PASSWORD)
    resp = client.search('Pepito', 'Cuenca', '')
    assert resp['resumen']['num_registros'] == '0'


@vcr.use_cassette()
def test_search():

    client = Client(URL, USER, PASSWORD)
    resp = client.search('Andres', 'Lopez', 'Obrador')
    assert resp['resumen']['num_registros'] != '0'
    assert resp['persons'] is not None

