from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import Investment


class Donation(Investment):
    user_id = Column(
        Integer,
        ForeignKey('user.id')
    )
    comment = Column(
        Text,
    )
