from pydantic import BaseModel, ConfigDict, Field, model_validator


class Person(BaseModel):
    lista: str = Field(alias='LISTA')
    coincidencia: int = Field(alias='COINCIDENCIA')
    nombrecomp: str = Field(alias='NOMBRECOMP')
    id_persona: str | None = Field(default=None, alias='ID_PERSONA')
    nombre: str | None = Field(default=None, alias='NOMBRE')
    paterno: str | None = Field(default=None, alias='PATERNO')
    materno: str | None = Field(default=None, alias='MATERNO')
    curp: str | None = Field(default=None, alias='CURP')
    rfc: str | None = Field(default=None, alias='RFC')
    fecha_nacimiento: str | None = Field(
        default=None, alias='FECHA_NACIMIENTO'
    )
    sexo: str | None = Field(default=None, alias='SEXO')
    metadata: dict = Field(default_factory=dict, alias='METADATA')

    model_config = ConfigDict(
        populate_by_name=True,
        extra='allow',
    )

    @model_validator(mode='after')
    def collect_extra_fields(self):
        if self.model_extra:
            self.metadata.update(self.model_extra)
        return self
