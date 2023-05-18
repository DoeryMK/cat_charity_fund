from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.consts import (
    PROJECT_NAME_OCCUPIED, DUPLICATE_VALIDATION_ATTRIBUTE,
    PROJECT_NOT_FOUND, PROJECT_CLOSED,
    FULL_AMOUNT_INVALID, PROJECT_CANT_BE_DELETED
)
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
        project_id: Optional[int] = None,
) -> None:
    if project_id:
        project = await charity_project_crud.get_by_name(
            project_id, project_name, session
        )
    else:
        project = await charity_project_crud.get_by_attribute(
            DUPLICATE_VALIDATION_ATTRIBUTE, project_name, session
        )
    if project:
        raise HTTPException(
            status_code=422,
            detail=PROJECT_NAME_OCCUPIED,
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )
    if not project:
        raise HTTPException(
            status_code=404,
            detail=PROJECT_NOT_FOUND,
        )
    return project


async def check_project_before_edit(
        project_id: int,
        object_in: CharityProjectUpdate,
        session: AsyncSession
) -> CharityProject:
    charity_project = await check_project_exists(
        project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=422,
            detail=PROJECT_CLOSED,
        )
    if (
            object_in.full_amount and
            object_in.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=422,
            detail=FULL_AMOUNT_INVALID,
        )
    if object_in.name:
        await check_project_name_duplicate(
            object_in.name, session, project_id
        )
    return charity_project


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await check_project_exists(
        project_id, session
    )
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail=PROJECT_CANT_BE_DELETED,
        )
    return charity_project
