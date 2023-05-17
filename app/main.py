from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    docs_url='/swagger',
    redoc_url='/redoc',
)