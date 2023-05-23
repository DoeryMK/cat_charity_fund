from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.consts import TABLE_NAME_DONATION
from app.models.abstract import Investment

REPRESENTATION = (
    '{table_name} от пользователя {user_name}. {super}'
)


class Donation(Investment):
    __table_name__ = TABLE_NAME_DONATION
    user_id = Column(
        Integer,
        ForeignKey('user.id')
    )
    comment = Column(
        Text,
    )

    def __repr__(self):
        return REPRESENTATION.format(
            table_name=self.__table_name__,
            user_name=self.user_id,
            super=super().__repr__(),
        )
