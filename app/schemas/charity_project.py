from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.core.consts import (
    FULL_AMOUNT_LESS_THAN_MIN, FULL_AMOUNT_MIN,
    PROJECT_NAME_CANT_BE_NONE
)


class CharityProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        max_length=100,
    )
    description: str
    full_amount: int = Field(
        ...,
        ge=1,
    )

    @validator('name')
    def name_cant_be_none(cls, value: str):
        if value == "" or value is None:
            raise ValueError(
                PROJECT_NAME_CANT_BE_NONE
            )
        return value


class CharityProjectUpdate(CharityProjectBase):

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
