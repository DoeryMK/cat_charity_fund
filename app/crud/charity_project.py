from typing import Dict, List, Union

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[Dict[str, Union[str, float]]]:
        query = select(
            [
                CharityProject.name,
                (
                    func.julianday(
                        CharityProject.close_date
                    ) - func.julianday(
                        CharityProject.create_date
                    )
                ).label('duration'),
                CharityProject.description
            ]
        ).where(
            CharityProject.fully_invested
        ).order_by(
            'duration'
        )
        projects = await session.execute(query)
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
