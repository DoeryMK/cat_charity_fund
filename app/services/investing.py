from datetime import datetime
from typing import List

from app.models.abstract import Investment


def add_invested_amount(
        investment: Investment,
        amount: int,
):
    investment.invested_amount += amount
    investment.fully_invested = (
        investment.invested_amount == investment.full_amount
    )
    if investment.fully_invested:
        investment.close_date = datetime.utcnow()


def investing_process(
        target: Investment,
        sources: List[Investment],
) -> List[Investment]:
    if not sources:
        return [target]
    updated_objects = []
    if target.invested_amount is None:  # Костыль для тестов
        target.invested_amount = 0
    for source in sources:
        available_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        add_invested_amount(source, available_amount)
        updated_objects.append(source)
        add_invested_amount(target, available_amount)
        if target.fully_invested:
            break
    updated_objects.append(target)
    return updated_objects
