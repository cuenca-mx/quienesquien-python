from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    model_validator,
)


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

    model_config = ConfigDict(
        populate_by_name=True,
        extra='allow',
    )

    @computed_field  # type: ignore[misc]
    @property
    def peso1(self) -> str:
        # peso1 is required for backward compatibility with previous version.
        return str(self.coincidencia)

    @model_validator(mode='after')
    def collect_extra_fields(self):
        if self.model_extra:
            lowercase_extra = {
                k.lower(): v for k, v in self.model_extra.items()
            }
            self.model_extra.clear()
            self.model_extra.update(lowercase_extra)
        return self
