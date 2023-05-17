from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey

from app.models.abstract import AbstractBase


class Donation(AbstractBase):
    user_id = Column(
        Integer,
        ForeignKey('user.id')
    )
    comment = Column(
        Text,
    )
