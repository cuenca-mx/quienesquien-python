from pydantic import BaseModel, ConfigDict, Field


class Person(BaseModel):
    id_persona: str | None = Field(default=None, alias='ID_PERSONA')
    coincidencia: int | None = Field(default=None, alias='COINCIDENCIA')
    nombre: str | None = Field(default=None, alias='NOMBRE')
    paterno: str | None = Field(default=None, alias='PATERNO')
    materno: str | None = Field(default=None, alias='MATERNO')
    curp: str | None = Field(default=None, alias='CURP')
    rfc: str | None = Field(default=None, alias='RFC')
    fecha_nacimiento: str | None = Field(
        default=None, alias='FECHA_NACIMIENTO'
    )
    sexo: str | None = Field(default=None, alias='SEXO')
    lista: str | None = Field(default=None, alias='LISTA')
    estatus: str | None = Field(default=None, alias='ESTATUS')
    dependencia: str | None = Field(default=None, alias='DEPENDENCIA')
    puesto: str | None = Field(default=None, alias='PUESTO')
    area: str | None = Field(default=None, alias='AREA')
    iddispo: int | None = Field(default=None, alias='IDDISPO')
    idrel: str | None = Field(default=None, alias='IDREL')
    parentesco: str | None = Field(default=None, alias='PARENTESCO')
    razonsoc: str | None = Field(default=None, alias='RAZONSOC')
    rfcmoral: str | None = Field(default=None, alias='RFCMORAL')
    issste: str | None = Field(default=None, alias='ISSSTE')
    imss: str | None = Field(default=None, alias='IMSS')
    ingresos: str | None = Field(default=None, alias='INGRESOS')
    nombrecomp: str | None = Field(default=None, alias='NOMBRECOMP')
    apellidos: str | None = Field(default=None, alias='APELLIDOS')
    entidad: str | None = Field(default=None, alias='ENTIDAD')
    imagen: str | None = Field(default=None, alias='IMAGEN')
    periodo: str | None = Field(default=None, alias='PERIODO')
    expediente: str | None = Field(default=None, alias='EXPEDIENTE')
    fecha_resolucion: str | None = Field(
        default=None, alias='FECHA_RESOLUCION'
    )
    causa_irregularidad: str | None = Field(
        default=None, alias='CAUSA_IRREGULARIDAD'
    )
    sancion: str | None = Field(default=None, alias='SANCION')
    fecha_cargo_ini: str | None = Field(default=None, alias='FECHA_CARGO_INI')
    fecha_cargo_fin: str | None = Field(default=None, alias='FECHA_CARGO_FIN')
    duracion: str | None = Field(default=None, alias='DURACION')
    monto: str | None = Field(default=None, alias='MONTO')
    autoridad_sanc: str | None = Field(default=None, alias='AUTORIDAD_SANC')
    admon_local: str | None = Field(default=None, alias='ADMON_LOCAL')
    numord: str | None = Field(default=None, alias='NUMORD')
    rubro: str | None = Field(default=None, alias='RUBRO')
    central_obrera: str | None = Field(default=None, alias='CENTRAL_OBRERA')
    numsocios: str | None = Field(default=None, alias='NUMSOCIOS')
    fecha_vigencia: str | None = Field(default=None, alias='FECHA_VIGENCIA')
    titulo: str | None = Field(default=None, alias='TITULO')
    domicilio_a: str | None = Field(default=None, alias='DOMICILIO_A')
    domicilio_b: str | None = Field(default=None, alias='DOMICILIO_B')
    colonia: str | None = Field(default=None, alias='COLONIA')
    cp: str | None = Field(default=None, alias='CP')
    ciudad: str | None = Field(default=None, alias='CIUDAD')
    lada: str | None = Field(default=None, alias='LADA')
    telefono: str | None = Field(default=None, alias='TELEFONO')
    fax: str | None = Field(default=None, alias='FAX')
    email: str | None = Field(default=None, alias='EMAIL')
    pais: str | None = Field(default=None, alias='PAIS')
    idrequerimiento: str | None = Field(default=None, alias='IDREQUERIMIENTO')
    fechaoficio: str | None = Field(default=None, alias='FECHAOFICIO')
    buscado_en: str | None = Field(default=None, alias='BUSCADO_EN')
    ciudadania: str | None = Field(default=None, alias='CIUDADANIA')
    pasaporte: str | None = Field(default=None, alias='PASAPORTE')
    cedula: str | None = Field(default=None, alias='CEDULA')
    nss: str | None = Field(default=None, alias='NSS')
    sancion_info: str | None = Field(default=None, alias='SANCION_INFO')
    ine: str | None = Field(default=None, alias='INE')
    italian_fiscal_code: str | None = Field(
        default=None, alias='ITALIAN_FISCAL_CODE'
    )
    registration_id: str | None = Field(default=None, alias='REGISTRATION_ID')
    national_foreign_id: str | None = Field(
        default=None, alias='NATIONAL_FOREIGN_ID'
    )
    vat_num: str | None = Field(default=None, alias='VAT_NUM')
    serial_num: str | None = Field(default=None, alias='SERIAL_NUM')
    kenyan_id: str | None = Field(default=None, alias='KENYAN_ID')
    dni: str | None = Field(default=None, alias='DNI')
    member_eta: str | None = Field(default=None, alias='MEMBER_ETA')
    operations_in: str | None = Field(default=None, alias='OPERATIONS_IN')
    icty: str | None = Field(default=None, alias='ICTY')
    registered_charity_no: str | None = Field(
        default=None, alias='REGISTERED_CHARITY_NO'
    )
    legal_situation: str | None = Field(default=None, alias='LEGAL_SITUATION')
    bosian_personal_id: str | None = Field(
        default=None, alias='BOSIAN_PERSONAL_ID'
    )
    parentesco_con: str | None = Field(default=None, alias='PARENTESCO_CON')
    le_number: str | None = Field(default=None, alias='LE_NUMBER')
    ruc_number: str | None = Field(default=None, alias='RUC_NUMBER')
    certificate_no: str | None = Field(default=None, alias='CERTIFICATE_NO')
    personal_id_card: str | None = Field(
        default=None, alias='PERSONAL_ID_CARD'
    )
    federal_id_card: str | None = Field(default=None, alias='FEDERAL_ID_CARD')
    visa_num: str | None = Field(default=None, alias='VISA_NUM')
    nuit: str | None = Field(default=None, alias='NUIT')
    nie: str | None = Field(default=None, alias='NIE')
    cif: str | None = Field(default=None, alias='CIF')
    cuip: str | None = Field(default=None, alias='CUIP')
    crn: str | None = Field(default=None, alias='CRN')
    fol_merc: str | None = Field(default=None, alias='FOL_MERC')
    cr_no: str | None = Field(default=None, alias='CR_NO')
    trukish_id_num: str | None = Field(default=None, alias='TRUKISH_ID_NUM')
    tribal_member: str | None = Field(default=None, alias='TRIBAL_MEMBER')
    refugee_id_card: str | None = Field(default=None, alias='REFUGEE_ID_CARD')
    resident_can: str | None = Field(default=None, alias='RESIDENT_CAN')
    cnp: str | None = Field(default=None, alias='CNP')
    rif: str | None = Field(default=None, alias='RIF')
    aircraft: str | None = Field(default=None, alias='AIRCRAFT')
    interpol_red_notice: str | None = Field(
        default=None, alias='INTERPOL_RED_NOTICE'
    )
    rtn: str | None = Field(default=None, alias='RTN')
    sre: str | None = Field(default=None, alias='SRE')
    company_num: str | None = Field(default=None, alias='COMPANY_NUM')
    public_reg_num: str | None = Field(default=None, alias='PUBLIC_REG_NUM')
    chinese_commercial_code: str | None = Field(
        default=None, alias='CHINESE_COMMERCIAL_CODE'
    )
    gov_gaz_num: str | None = Field(default=None, alias='GOV_GAZ_NUM')
    cer_incorp_num: str | None = Field(default=None, alias='CER_INCORP_NUM')
    dubai_cha_comm_mem: str | None = Field(
        default=None, alias='DUBAI_CHA_COMM_MEM'
    )
    vessel_num: str | None = Field(default=None, alias='VESSEL')
    mmsi: str | None = Field(default=None, alias='MMSI')
    international_id: str | None = Field(
        default=None, alias='INTERNATIONAL_ID'
    )
    identification_no: str | None = Field(
        default=None, alias='IDENTIFICACION_NO'
    )
    residente_no: str | None = Field(default=None, alias='RESIDENTE_NO')
    licencia_cond: str | None = Field(default=None, alias='LICENCIA_COND')
    cartilla_no: str | None = Field(default=None, alias='CARTILLA_NO')
    cuit: str | None = Field(default=None, alias='CUIT')
    nit: str | None = Field(default=None, alias='NIT')
    business_reg_num: str | None = Field(
        default=None, alias='BUSINESS_REG_NUM'
    )
    us_fein: str | None = Field(default=None, alias='US_FEIN')
    taxid: str | None = Field(default=None, alias='TAXID')
    web: str | None = Field(default=None, alias='WEB')
    matricula_merc: str | None = Field(default=None, alias='MATRICULA_MERC')
    gafi: str | None = Field(default=None, alias='GAFI')
    repife: str | None = Field(default=None, alias='REPIFE')
    oced: str | None = Field(default=None, alias='OCED')
    organismos: str | None = Field(default=None, alias='ORGANISMOS')
    nombrecompsndx: str | None = Field(default=None, alias='nombrecompsndx')
    ncampos: str | None = Field(default=None, alias='ncampos')
    relacionados: str | None = Field(default=None, alias='RELACIONADOS')
    disposicion: str | None = Field(default=None, alias='DISPOSICION')
    categoria_riesgo: str | None = Field(
        default=None, alias='CATEGORIA_RIESGO'
    )
    cat_ingresos: str | None = Field(default=None, alias='CAT_INGRESOS')
    organo: str | None = Field(default=None, alias='ORGANO')
    texto: str | None = Field(default=None, alias='TEXTO')
    facebook_descripcion: str | None = Field(
        default=None, alias='facebook_DESCRIPCION'
    )
    instagram_descripcion: str | None = Field(
        default=None, alias='instagram_DESCRIPCION'
    )
    linkedin_descripcion: str | None = Field(
        default=None, alias='linkedin_DESCRIPCION'
    )
    twitter_descripcion: str | None = Field(
        default=None, alias='twitter_DESCRIPCION'
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )
