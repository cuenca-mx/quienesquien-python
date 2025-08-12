import datetime as dt
from typing import Any

import pytest

from quienesquien.person import Person


def test_collect_extra_fields() -> None:
    person_data: dict[str, Any] = {
        'LISTA': 'lista1',
        'COINCIDENCIA': 100,
        'NOMBRECOMP': 'Juan Pérez',
        'CAMPO_EXTRA1': 'valor1',
        'CAMPO_EXTRA2': 'valor2',
    }
    person = Person(**person_data)
    assert person.lista == 'lista1'
    assert person.peso1 == '100'
    assert person.coincidencia == 100
    assert person.nombrecomp == 'Juan Pérez'

    # Access extra fields through model_extra after lowercase conversion
    assert person.model_extra is not None
    assert person.model_extra['campo_extra1'] == 'valor1'
    assert person.model_extra['campo_extra2'] == 'valor2'


@pytest.mark.parametrize(
    "fecha_nacimiento_input, expected_fecha_nacimiento, expected_date",
    [
        ('13/11/1953', '13/11/1953', dt.date(1953, 11, 13)),
        (None, None, None),
        ('', '', None),
        ('invalid-date', 'invalid-date', None),
        ('1953-11-13', '1953-11-13', None),
        ('13/11', '13/11', None),
        ('13-11-1953', '13-11-1953', None),
    ],
)
def test_fecha_nacimiento_date(
    fecha_nacimiento_input: str | None,
    expected_fecha_nacimiento: str | None,
    expected_date: dt.date | None,
) -> None:
    person_data: dict[str, Any] = {
        'LISTA': 'PPE',
        'COINCIDENCIA': 100,
        'NOMBRECOMP': 'Andres Manuel López Obrador',
        'FECHA_NACIMIENTO': fecha_nacimiento_input,
    }
    person = Person(**person_data)

    assert person.fecha_nacimiento == expected_fecha_nacimiento
    assert person.fecha_nacimiento_date == expected_date
