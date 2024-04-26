from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas import User
from ..dependencies.user import get_current_user
from ..dependencies.meal import get_current_user_meals

router = APIRouter()


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/me/meals")
async def read_own_meals(
    current_user: Annotated[User, Depends(get_current_user)],
):
    meals = get_current_user_meals(current_user)
    return meals
