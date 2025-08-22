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
    'fecha_nacimiento_input, expected_date',
    [
        ('13/11/1953', dt.date(1953, 11, 13)),
        (None, None),
        ('', None),
        ('invalid-date', None),
        ('1953-11-13', None),
        ('13/11', None),
        ('13-11-1953', None),
    ],
)
def test_fecha_nacimiento_date(
    fecha_nacimiento_input: str | None,
    expected_date: dt.date | None,
) -> None:
    person_data: dict[str, Any] = {
        'LISTA': 'PPE',
        'COINCIDENCIA': 100,
        'NOMBRECOMP': 'Andres Manuel López Obrador',
        'FECHA_NACIMIENTO': fecha_nacimiento_input,
    }
    person = Person(**person_data)

    assert person.fecha_nacimiento == fecha_nacimiento_input
    assert person.fecha_nacimiento_to_date == expected_date


@pytest.mark.parametrize(
    'p_nacimiento, p_curp, input_date, input_curp, expected_result',
    [
        # Different birth dates
        ('13/11/1953', None, dt.date(1953, 11, 14), None, False),
        # Same birth dates
        ('13/11/1953', None, dt.date(1953, 11, 13), None, True),
        # Different CURPs
        (None, 'LOOA531113HDFPBR07', None, 'DIFFERENT_CURP_123', False),
        # Same CURPs
        (None, 'LOOA531113HDFPBR07', None, 'LOOA531113HDFPBR07', True),
        # Different birth dates and same curp
        (
            '13/11/1953',
            'LOOA531113HDFPBR07',
            dt.date(1953, 11, 14),
            'LOOA531113HDFPBR07',
            True,
        ),
        # Same birth dates and different curp
        (
            '13/11/1953',
            'LOOA531113HDFPBR07',
            dt.date(1953, 11, 13),
            'DIFFERENT_CURP_123',
            True,
        ),
        # Both date and CURP different
        (
            '13/11/1953',
            'LOOA531113HDFPBR07',
            dt.date(1953, 11, 14),
            'DIFFERENT_CURP_123',
            False,
        ),
        # Both date and CURP same
        (
            '13/11/1953',
            'LOOA531113HDFPBR07',
            dt.date(1953, 11, 13),
            'LOOA531113HDFPBR07',
            True,
        ),
        # No data to compare
        (None, None, None, None, False),
        # Person has data but no input data
        ('13/11/1953', None, None, None, False),
        (None, 'LOOA531113HDFPBR07', None, None, False),
        ('13/11/1953', 'LOOA531113HDFPBR07', None, None, False),
        # Input data but person has no data
        (None, None, dt.date(1953, 11, 13), 'LOOA531113HDFPBR07', False),
    ],
)
def test_matches_data(
    p_nacimiento: str | None,
    p_curp: str | None,
    input_date: dt.date | None,
    input_curp: str | None,
    expected_result: bool,
) -> None:
    person_data: dict[str, Any] = {
        'LISTA': 'PPE',
        'COINCIDENCIA': 90,
        'NOMBRECOMP': 'Test Person',
    }

    if p_nacimiento is not None:
        person_data['FECHA_NACIMIENTO'] = p_nacimiento

    if p_curp is not None:
        person_data['CURP'] = p_curp

    person = Person(**person_data)

    result = person.matches_data(date_of_birth=input_date, curp=input_curp)
    assert result == expected_result
