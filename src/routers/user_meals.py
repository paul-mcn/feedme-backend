from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.aws import deserialize_item

from ..dependencies.dates import get_start_of_week
from ..dependencies.meal_recommendations import (
    create_recommended_meals,
    get_recommended_meals,
)
from ..schemas import MealCreate, MealIn, User, MealSnapshotRequestBody
from urllib.parse import quote
from ..dependencies.user import get_current_user
from ..dependencies.meal import (
    create_current_user_meal,
    get_current_user_meals,
    get_meal_snapshot,
    get_raw_current_user_meals,
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
    response = get_raw_current_user_meals(current_user.id, limit=7)
    if response.get("Count") < 7:
        raise HTTPException(
            status_code=409, detail="Not enough meals to create recommendations"
        )
    serialized_meals = response.get("Items")
    deserialized_meals = [MealIn(**deserialize_item(meal)) for meal in serialized_meals]
    recommendations = create_recommended_meals(
        current_user.id, deserialized_meals, week_start_date
    )
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
