from fastapi import APIRouter

from app.services import personas

router = APIRouter(prefix="/api/personas", tags=["personas"])


@router.get("")
def get_personas():
    return personas.list_personas()
