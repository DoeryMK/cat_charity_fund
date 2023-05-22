from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, Column,
    DateTime, Integer
)

from app.core.consts import INVESTED_AMOUNT_DEFAULT
from app.core.db import Base

REPRESENTATION = (
    'Дата создания - {create_date}, '
    'Общая сумма - {full_amount}, '
    'Инвестировано - {invested_amount}.'
)


class Investment(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='full_amount_is_positive'
        ),
        CheckConstraint(
            'full_amount >= invested_amount',
            name='full_amount_ge_invested_amount'
        )
    )
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

    def __repr__(self):
        return REPRESENTATION.format(
            create_date=self.create_date,
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
        )
