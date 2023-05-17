from sqlalchemy import Column, String, Text

from app.core.consts import PROJECT_NAME_LENGTH
from app.models.abstract import AbstractBase


class CharityProject(AbstractBase):
    name = Column(
        String(PROJECT_NAME_LENGTH),
        unique=True,
        nullable=False
    )
    description = Column(
        Text,
        nullable=False
    )
