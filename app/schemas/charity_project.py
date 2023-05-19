from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator, Extra, root_validator

from app.core.consts import (
    PROJECT_NAME_CANT_BE_NONE, FULL_AMOUNT_MIN,
    FULL_AMOUNT_LESS_THAN_MIN, PROJECT_FIELDS_CANT_BE_EMPTY
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
    description: str = Field(
        ...,
        min_length=1,
    )
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

    @root_validator(skip_on_failure=True)
    def value_cant_be_empty(cls, values):
        for _, value in values.items():
            if value == "":
                raise ValueError(
                    PROJECT_FIELDS_CANT_BE_EMPTY
                )
        return values

    # TO DO: Валидацию для целых чисел больше нуля можно не писать:
    # посмотреть в документации pydantic
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
