from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime

from app.core.consts import INVESTED_AMOUNT_DEFAULT
from app.core.db import Base


class AbstractBase(Base):
    __abstract__ = True

    full_amount = Column(
        Integer,
    )
    invested_amount = Column(
        Integer,
        default=INVESTED_AMOUNT_DEFAULT,
    )
    fully_invested = Column(
        Boolean,
        default=False,
    )
    create_date = Column(
        DateTime,
        index=True,
        default=datetime.utcnow
    )
    close_date = Column(
        DateTime,
        index=True,
        default=None
    )
