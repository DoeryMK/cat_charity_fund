from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(
    CRUDBase[
        CharityProject, CharityProjectCreate
    ]
):

    async def get_by_name(
            self,
            project_id: int,
            project_name: str,
            session: AsyncSession
    ) -> CharityProject:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name,
                CharityProject.id != project_id
            )
        )
        return projects.scalars().first()

    async def update(
            self,
            db_project: CharityProject,
            project_in: CharityProjectUpdate,
            session: AsyncSession,
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_project)
        update_data = project_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_project, field, update_data[field])
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project


charity_project_crud = CRUDCharityProject(CharityProject)
