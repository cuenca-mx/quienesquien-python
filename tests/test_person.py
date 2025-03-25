from quienesquien.person import Person


def test_collect_extra_fields():
    person_data = {
        'LISTA': 'lista1',
        'COINCIDENCIA': 100,
        'NOMBRECOMP': 'Juan Pérez',
        'CAMPO_EXTRA1': 'valor1',
        'CAMPO_EXTRA2': 'valor2',
    }
    person = Person(**person_data)
    assert person.metadata == {
        'campo_extra1': 'valor1',
        'campo_extra2': 'valor2',
    }
    assert not person.model_extra
    assert person.lista == 'lista1'
    assert person.coincidencia == 100
    assert person.nombrecomp == 'Juan Pérez'
