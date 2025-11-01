from datetime import date

from pydantic import BaseModel, Field


class PersonBase(BaseModel):
    sosa: int = Field(gt=0)
    sex: str = Field(pattern="^[MF]$")
    full_name: str
    birth: date | None = None
    death: date | None = None
    place: str | None = None
    description: str | None = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    sex: str | None = Field(default=None, pattern="^[MF]$")
    full_name: str | None = None
    birth: date | None = None
    death: date | None = None
    place: str | None = None
    description: str | None = None


class PersonOut(PersonBase):
    generation: int
