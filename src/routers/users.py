from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas import User
from ..dependencies import get_current_user, get_current_active_user, fake_meals_db


router = APIRouter()


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/me/meals")
async def read_own_meals(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return {"meals": fake_meals_db}
