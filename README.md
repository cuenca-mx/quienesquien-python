# quienesquien

[![test](https://github.com/cuenca-mx/quienesquien-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/quienesquien-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/quienesquien-python/branch/master/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/quienesquien-python)
[![PyPI](https://img.shields.io/pypi/v/quienesquien.svg)](https://pypi.org/project/quienesquien/)

Cliente para el servicio de listas de Quienesquien (https://app.q-detect.com/)

## Instalación

```bash
pip install quienesquien
```

## Uso

```python
from quienesquien import Client

client = Client(URL, USER, CLIENT_ID, SECRET_ID)

try:
    response = client.search('Juan', 'Lopez', 'Perez')

    if response.get('resumen', {}).get('success'):
        persons = [vars(person) for person in response.get('persons', [])]
        print(persons)
except Exception as e:
    print(f"Error during search: {e}")
```