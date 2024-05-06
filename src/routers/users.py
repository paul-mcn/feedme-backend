from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas import MealCreate, User
from ..dependencies.user import get_current_user
from ..dependencies.meal import get_current_user_meals, put_current_user_meal

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


@router.post("/me/meals/add")
async def create_own_meal(
    current_user: Annotated[User, Depends(get_current_user)], meal: MealCreate
):

    # TODO: web scrape url to get ingredients, title, and other info
    # for automatic form filling

    response = put_current_user_meal(current_user.id, meal)
    return response
