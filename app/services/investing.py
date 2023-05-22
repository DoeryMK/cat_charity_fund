from datetime import datetime
from typing import Optional, Union, List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import CRUDCharityProject
from app.crud.donation import CRUDonation
from app.models import CharityProject, Donation
from app.models.abstract import Investment


def update_attrs(
        db_object: Union[CharityProject, Donation],
        amount: Optional[int] = None
):
    if amount is not None:
        setattr(db_object, 'invested_amount', amount)
    else:
        setattr(db_object, 'invested_amount', db_object.full_amount)
        setattr(db_object, 'fully_invested', True)
        setattr(db_object, 'close_date', datetime.utcnow())


async def investing_process(
        investment: Union[CharityProject, Donation],
        investment_object: Union[CRUDCharityProject, CRUDonation],
        session: AsyncSession,
) -> Union[CharityProject, Donation]:
    input_amount = investment.full_amount
    queue = []
    while input_amount > 0:
        db_object = await investment_object.get_first_created(
            session
        )
        if not db_object:
            break
        amount = db_object.invested_amount + input_amount
        if amount < db_object.full_amount:
            update_attrs(
                db_object,
                amount=amount
            )
            input_amount = 0
        elif amount >= db_object.full_amount:
            input_amount -= db_object.full_amount - db_object.invested_amount
            update_attrs(db_object)
        queue.append(db_object)
    if input_amount == 0:
        update_attrs(investment)
    elif input_amount:
        update_attrs(
            investment,
            amount=investment.full_amount - input_amount
        )
    queue.append(investment)
    session.add_all(queue)
    await session.commit()
    for obj in queue:
        await session.refresh(obj)
    return investment


def close_investing(investment: Investment):
    investment.invested_amount = investment.full_amount
    investment.fully_invested = True
    investment.close_date = datetime.utcnow()


def new_investing_process(
        target: Investment,
        sources: List[Investment],
) -> List[Investment]:
    updated_objects = []
    if not sources:
        return list(target)
    for source in sources:
        delta = min(source.full_amount - source.invested_amount,
                    target.full_amount - target.invested_amount)
        source.invested_amount += delta
        if source.invested_amount == source.full_amount:
            close_investing(source)
        updated_objects.append(source)
        target.invested_amount += delta
        if target.invested_amount == target.full_amount:
            close_investing(target)
            break
    updated_objects.append(target)
    return updated_objects
