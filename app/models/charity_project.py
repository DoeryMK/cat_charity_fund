from sqlalchemy import Column, String, Text

from app.core.consts import PROJECT_NAME_LENGTH, TABLE_NAME_CHARITY_PROJECT
from app.models.abstract import Investment

REPRESENTATION = '{table_name}: {name}. {super}'


class CharityProject(Investment):
    __table_name__ = TABLE_NAME_CHARITY_PROJECT
    name = Column(
        String(PROJECT_NAME_LENGTH),
        unique=True,
        nullable=False
    )
    description = Column(
        Text,
        nullable=False
    )

    def __repr__(self):
        return REPRESENTATION.format(
            table_name=self.__table_name__,
            name=self.name,
            super=super().__repr__(),
        )
