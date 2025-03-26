# quienesquien

[![test](https://github.com/cuenca-mx/quienesquien-python/workflows/test/badge.svg)](https://github.com/cuenca-mx/quienesquien-python/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/quienesquien-python/branch/master/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/quienesquien-python)
[![PyPI](https://img.shields.io/pypi/v/quienesquien.svg)](https://pypi.org/project/quienesquien/)

Client for the Quienesquien list service (https://app.q-detect.com/)

> [!IMPORTANT]
> Generating a new authentication token automatically invalidates any previously created tokens.
> If multiple applications or services are using the same credentials, creating a new token will render the old ones invalid, potentially causing other applications to fail.
> To avoid issues, reuse an existing token whenever possible by storing it in an environment variable or a secure location.

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

## Token Generation

Before performing searches, you need to create an authentication token using the create_token method:

```python
from quienesquien import Client

auth_token = await Client.create_token(os.environ['QEQ_CLIENT_ID'], os.environ['QEQ_SECRET_ID'])
```

You can reuse this token in subsequent requests.

## Example

Once you have the token, you can perform searches by passing it:

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

auth_token = await Client.create_token(os.environ['QEQ_CLIENT_ID'], os.environ['QEQ_SECRET_ID'])

client = Client(
    os.environ['QEQ_USER'],
    auth_token,
)

try:
    persons = await client.search(
        full_name='Andres Manuel Lopez Obrador',
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

## Environment Variable (Optional)

To simplify usage, you can store the token in an environment variable:

```bash
export QEQ_AUTH_TOKEN=your_auth_token
```

Then, instantiate the client using the environment variable:

```python
import os

client = Client(
    os.environ['QEQ_USER'],
    os.environ['QEQ_CLIENT_ID'],
    os.environ.get('QEQ_AUTH_TOKEN'),
)
```

## Search Parameters
- `full_name` (str): Full name of the person.
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
You must specify at least one search parameter: full_name, rfc or curp.

## Response Structure
- `persons` (list): List of matched persons.
