from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas import MealCreate, User, MealSnapshotRequestBody
from urllib.parse import quote
from ..dependencies.user import get_current_user
from ..dependencies.meal import (
    create_current_user_meal,
    get_current_user_meals,
    get_meal_snapshot,
    get_meal_recommendations,
)

router = APIRouter()


@router.get("")
async def read_own_meals(
    current_user: Annotated[User, Depends(get_current_user)],
):
    meals = get_current_user_meals(current_user.id)
    return meals


@router.get("/recommendations")
async def read_own_meal_recommendations(
    current_user: Annotated[User, Depends(get_current_user)],
):
    meals = get_meal_recommendations(current_user.id)
    return meals


@router.post("/add")
async def create_own_meal(
    current_user: Annotated[User, Depends(get_current_user)], meal: MealCreate
):

    # TODO: web scrape url to get ingredients, title, and other info
    # for automatic form filling

    response = create_current_user_meal(current_user.id, meal)
    return response


@router.post("/snapshot")
async def upsert_meal_snapshot(
    url: MealSnapshotRequestBody,
    current_user: Annotated[User, Depends(get_current_user)],
):
    snapshotUrl = quote(url.url)
    meal = get_meal_snapshot(snapshotUrl)
    if meal is None:
        return {"meal": None}

    # TODO: web scrape url to get ingredients, title, and other info
    # for automatic form filling

    return {"meal": meal}
