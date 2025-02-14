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
from quienesquien.enums import Gender, SearchList, SearchType
from quienesquien.exc import (
    InsufficientBalanceError,
    InvalidPlanError,
    InvalidTokenError,
    PersonNotFoundError,
)

client = Client(
    os.environ['QEQ_USER'],
    os.environ['QEQ_CLIENT_ID'],
    os.environ['QEQ_SECRET_ID'],
)

try:
    persons = await client.search(
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
except InsufficientBalanceError:
    print('Saldo insuficiente')
except InvalidPlanError:
    print('Plan inválido')
except InvalidTokenError:
    print('Token inválido')
except PersonNotFoundError:
    persons = []
```

## Search Parameters
- `nombre` (str): First name(s) of the person.
- `paterno` (str): First surname.
- `materno` (str): Second surname.
- `match_score` (int): Minimum match percentage (default: 60).
- `rfc` (str): Mexican RFC.
- `curp` (str): Mexican CURP.
- `gender` (Gender): masculino or femenino.
- `birthday` (datetime.date): Date of birth.
- `search_type` (SearchType): fisica or moral.
- `search_list` (tuple[SearchList, ...]): Lists to search.
    If not provided, searches all.

The search follows a hierarchical approach: it first attempts to find a match using the RFC.
If no match is found, it searches by CURP. Finally, if neither is found, it looks for a match by name.
You must specify at least one search parameter: name (including first nombre, paterno and materno), RFC or CURP.

## Response Structure
- `persons` (list): List of matched persons.
