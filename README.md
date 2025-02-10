# quienesquien

[![test](https://github.com/cuenca-mx/quienesquien-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/quienesquien-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/quienesquien-python/branch/master/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/quienesquien-python)
[![PyPI](https://img.shields.io/pypi/v/quienesquien.svg)](https://pypi.org/project/quienesquien/)

Client for the Quienesquien list service (https://app.q-detect.com/)

## Installation

```bash
pip install quienesquien
```

## Development & Testing

The project configuration is managed through environment variables. Set them before running tests:
```bash
export $(<env.template)
```

To run unit tests, use `pytest`.
```bash
pytest
```

## Usage

Before using the client, configure the required environment variables:
```bash
export QEQ_USER=your_user
export QEQ_CLIENT_ID=your_client_id
export QEQ_SECRET_ID=your_secret_key
```

## Example
```python
import os
from quienesquien import Client

client = Client(
    os.environ['QEQ_USER'],
    os.environ['QEQ_CLIENT_ID'],
    os.environ['QEQ_SECRET_ID'],
)

response = await client.search(
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

if response.success:
    print(f'Found {response.num_registros} records')
    for person in response.persons:
        print(f'Name: {person.nombrecomp} - Match: {person.coincidencia}%')
else:
    print('No records found')

response = await client.search(
    nombre='Pepito',
    paterno='Cuenca',
    materno='',
    match_score=85,
)

if response.success:
    print(f'Found {response.num_registros} records')
    for person in response.persons:
        print(f'Name: {person.nombrecomp} - Match: {person.coincidencia}%')
else:
    print('No records found')
```

## Search Parameters
- `nombre` (required): First name(s), case and accent insensitive.
- `paterno` (required): First surname, case and accent insensitive.
- `materno` (required): Second surname, case and accent insensitive.
- `match_score` (optional): Minimum match percentage (default: 60).
- `rfc` (optional): Mexican RFC.
- `curp` (optional): Mexican CURP.
- `sex` (optional): Gender ('M' for male, 'F' for female).
- `birthday` (optional): Date of birth (dd/mm/yyyy).
- `search_type` (optional): Search type (0 for individuals, 1 for companies).
- `search_list` (optional): Comma-separated list of specific lists to search (e.g., 'PPE,PEPINT,VENC'). Defaults to all lists.

## Response Structure
- `success` (bool): `True` if the search was successful and records were found.
- `num_registros` (int): Number of records found.
- `persons` (list): List of matched persons.
