from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    description: Optional[str]
    full_amount: Optional[int] = Field(
        ...,
        min=1,
    )


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    description: str
    full_amount: int = Field(
        ...,
        min=1,
    )


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
