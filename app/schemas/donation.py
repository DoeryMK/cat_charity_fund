from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class DonationBase(BaseModel):
    full_amount: int = Field(
        ...,
        ge=1,
    )
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationShortDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationFullDB(DonationShortDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
