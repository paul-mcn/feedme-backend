from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.aws import deserialize_item

from ..dependencies.dates import get_start_of_week
from ..dependencies.meal_recommendations import (
    create_recommended_meals,
    get_recommended_meals,
)
from ..schemas import FollowMealRequest, MealIn, User, MealSnapshotRequest
from urllib.parse import quote
from ..dependencies.user import get_current_user
from ..dependencies.meal import (
    create_current_user_meal,
    get_current_user_meals,
    get_meal_snapshot,
    follow_meal,
)

router = APIRouter()


@router.get("")
async def read_own_meals(
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = 20,
    lastEvaluatedKey: str | None = None,
):
    meals = get_current_user_meals(current_user.id, limit, lastEvaluatedKey)
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
    user_meals = get_current_user_meals(current_user.id, limit=7)

    if len(user_meals.meals) < 7:
        raise HTTPException(
            status_code=409, detail="Not enough meals to create recommendations"
        )
    deserialized_meals = [
        MealIn(
            mealId=meal.id,
            title=meal.title,
            ingredients=meal.ingredients,
            time=meal.time,
            price=meal.price,
            imageURLs=meal.imageURLs,
            snapshotURL=meal.snapshotURL,
            notes=meal.notes,
            description=meal.description,
            follows=meal.follows,
        )
        for meal in user_meals.meals
    ]
    recommendations = create_recommended_meals(
        current_user.id, deserialized_meals, week_start_date
    )
    return recommendations


@router.post("/add")
async def create_own_meal(
    current_user: Annotated[User, Depends(get_current_user)],
    meal: Annotated[MealIn, Depends()],
):

    # TODO: web scrape url to get ingredients, title, and other info
    # for automatic form filling

    response = create_current_user_meal(current_user.id, meal)
    return response


@router.post("/follow")
async def user_follow_meal(
    meal: FollowMealRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    response = follow_meal(current_user.id, meal.mealId)
    return response


@router.post("/snapshot")
async def upsert_meal_snapshot(
    url: MealSnapshotRequest,
    current_user: Annotated[User, Depends(get_current_user)],
):
    snapshotUrl = quote(url.url)
    meal = get_meal_snapshot(snapshotUrl)
    if meal is None:
        return {"meal": None}

    # TODO: web scrape url to get ingredients, title, and other info
    # for automatic form filling

    return {"meal": meal}
