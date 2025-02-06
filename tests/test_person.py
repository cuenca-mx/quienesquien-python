from quienesquien import Person


def test_create_person_with_dict():
    data = {
        "nombrecomp": "Andres Manuel López Obrador",
        "curp": "LOOA531113HTCPBN07",
        "rfc": "LOOA531113F15",
        "id_persona": "QEQ0281252",
        "nombre": "Andres Manuel",
        "paterno": "López",
        "materno": "Obrador",
    }

    persona = Person(data)

    assert persona.__dict__ == data


def test_create_person_with_kwargs():
    kwargs = {
        "nombrecomp": "Andres Manuel López Obrador",
        "curp": "LOOA531113HTCPBN07",
        "rfc": "LOOA531113F15",
        "id_persona": "QEQ0281252",
        "nombre": "Andres Manuel",
        "paterno": "López",
        "materno": "Obrador",
    }

    persona = Person(**kwargs)

    assert persona.__dict__ == kwargs
