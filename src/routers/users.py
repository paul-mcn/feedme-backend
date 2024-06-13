from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.dependencies.meal import (
    batch_follow_meals,
    get_all_meals,
    get_current_user_meals,
)
from src.dependencies.env import get_environment_settings
from ..schemas import User
from ..dependencies.user import get_current_user
from .user_meals import router as meals_router

settings = get_environment_settings()

router = APIRouter()

router.include_router(meals_router, prefix="/me/meals", tags=["meals"])


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return User(
        id=current_user.id,
        email=current_user.email,
        firstName=current_user.firstName,
        lastName=current_user.lastName,
    )


@router.post("/me/setup-account")
async def setup_account(current_user: Annotated[User, Depends(get_current_user)]):
    user_meals = get_current_user_meals(current_user.id, limit=1)
    if len(user_meals.meals) > 0:
        return current_user

    try:
        meals = get_all_meals(limit=7)
        meal_ids = [meal.id for meal in meals.meals]
        batch_follow_meals(current_user.id, meal_ids)
    except IndexError:
        raise HTTPException(status_code=409, detail="No meals found")
    return current_user
