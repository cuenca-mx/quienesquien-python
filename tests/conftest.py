import pytest

from quienesquien import Client

URL = 'https://app.q-detect.com/'
USER = 'pepito@cuenca.com'
CLIENT_ID = '123456-1234-1234'
SECRET_ID = 'notsecurepassword'


@pytest.fixture
def client():
    yield Client(URL, USER, CLIENT_ID, SECRET_ID)
