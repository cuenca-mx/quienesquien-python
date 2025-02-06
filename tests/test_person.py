from quienesquien import Person


def test_create_person_with_dict():
    data = {
        'nombrecomp': 'John Doe Smith',
        'curp': 'TEST123456HDFXXX01',
        'rfc': 'TEST123456ABC',
        'id_persona': 'TEST12345',
        'nombre': 'John',
        'paterno': 'Doe',
        'materno': 'Smith',
    }

    persona = Person(data)

    assert persona.__dict__ == data


def test_create_person_with_kwargs():
    kwargs = {
        'nombrecomp': 'John Doe Smith',
        'curp': 'TEST123456HDFXXX01',
        'rfc': 'TEST123456ABC',
        'id_persona': 'TEST12345',
        'nombre': 'John',
        'paterno': 'Doe',
        'materno': 'Smith',
    }

    persona = Person(**kwargs)

    assert persona.__dict__ == kwargs
