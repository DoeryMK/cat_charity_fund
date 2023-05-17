"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base  # noqa
# Все модели теперь докода перепишем здесь импорты моделей в одну строку:
from app.models import CharityProject, Donation, User  # noqa