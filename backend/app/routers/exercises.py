from fastapi import APIRouter, Query

from app.core.config import settings
from app.services import exercises

router = APIRouter(prefix="/api/exercises", tags=["ejercicios"])


def _valid_language(language: str) -> str:
    if language not in settings.supported_languages:
        return "es-AR"
    return language


@router.get("")
def get_exercises(
    language: str = Query("es-AR"),
    level: str | None = Query(None, pattern="^(principiante|intermedio|avanzado)?$"),
):
    return exercises.list_exercises(_valid_language(language), level)


@router.get("/daily")
def get_daily_exercise(language: str = Query("es-AR")):
    return exercises.daily_exercise(_valid_language(language))
