from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator, Extra

from app.core.consts import (
    PROJECT_NAME_CANT_BE_NONE, FULL_AMOUNT_MIN,
    FULL_AMOUNT_LESS_THAN_MIN
)

class CharityProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    description: str
    full_amount: int = Field(
        ...,
        ge=1,
    )


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cant_be_None(cls, value: str):
        if value is None:
            raise ValueError(
                PROJECT_NAME_CANT_BE_NONE
            )
        return value

    @validator('full_amount')
    def full_amount_must_be_greater_than_zero(cls, value: str):
        if value < FULL_AMOUNT_MIN:
            raise ValueError(
                FULL_AMOUNT_LESS_THAN_MIN
            )
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
