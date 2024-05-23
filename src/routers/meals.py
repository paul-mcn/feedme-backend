from datetime import date
import json
from typing import Annotated
from fastapi import APIRouter, Depends

from ..dependencies.dates import get_start_of_week
from ..dependencies.meal_recommendations import (
    create_recommended_meals,
    get_recommended_meals,
    is_recommendation_expired,
)
from ..schemas import MealCreate, User, MealSnapshotRequestBody
from urllib.parse import quote
from ..dependencies.user import get_current_user
from ..dependencies.meal import (
    create_current_user_meal,
    get_current_user_meals,
    get_meal_snapshot,
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
    week_start_date: date | None = None,
):
    # if there is no date supplied then we just get the most recent entry
    week_start_date = get_start_of_week(week_start_date)
    recommendations = get_recommended_meals(current_user.id, week_start_date)
    return recommendations


@router.post("/create-recommendations")
async def create_own_meal_recommendations(
    current_user: Annotated[User, Depends(get_current_user)],
    week_start_date: date | None = None,
):
    # if there is no date supplied then we just get the most recent entry
    recommendations = create_recommended_meals(current_user.id, week_start_date)
    return recommendations


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
