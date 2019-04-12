
PERSON_FIELDNAMES = """
    id_persona
    peso1
    peso2
    nombre
    paterno
    materno
    curp
    rfc
    fecha_nacimiento
    sexo
    lista
    estatus
    dependencia
    puesto
    area
    iddispo
    idrel
    parentesco
    razonsoc
    rfcmoral
    issste
    imss
    ingresos
    nombrecomp
    apellidos
    entidad
    curp_ok
    periodo
    expediente
    fecha_resolucion
    causa_irregularidad
    sancion
    fecha_cargo_ini
    fecha_cargo_fin
    duracion
    monto
    autoridad_sanc
    admon_local
    numord
    rubro
    central_obrera
    numsocios
    fecha_vigencia
    titulo
    domicilio_a
    domicilio_b
    colonia
    cp
    ciudad
    lada
    telefono
    fax
    email
    pais
    idrequerimiento
    fechaoficio
    buscado_en
    ciudadania
    pasaporte
    cedula
    nss
    parentesco_con
    identificacion_no
    licencia_cond
    cartilla_no
    gafi
""".split()


class Person(object):
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
