from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas import User
from ..dependencies.user import get_current_user
from .meals import router as meals_router

router = APIRouter()

router.include_router(meals_router, prefix="/me/meals", tags=["meals"])


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
