from typing import Optional
from datetime import date, timedelta
import random
from src.dependencies.dates import get_start_of_week
from src.dependencies.meal import get_raw_current_user_meals
from src.types import DynamoDBQueryResponse
from ..schemas import (
    MealIn,
    MealRecommendation,
    MealRecommendationInDB,
    UserMealRecommendations,
)
from .aws import deserialize_item, dynamodb_client, serialize_item


def is_recommendation_expired(recommended_meals: list[MealRecommendation]):
    # get latest date without mutating original list
    latest_date = max([meal.date for meal in recommended_meals])
    return latest_date < date.today()


def format_key_from_date(date: date):
    return date.strftime("%Y-%m-%d")


def randomly_select_meals(meals: list, count: int):
    randomly_selected_meals = random.sample(meals, min(count, 7))
    return randomly_selected_meals


def put_recommended_meals(
    current_user_id: str,
    recommended_meals: list[MealRecommendation],
    week_start_date: date,
):
    serialized_meals = [
        {"M": serialize_item(meal.model_dump())} for meal in recommended_meals
    ]
    entityId = f"{current_user_id}#{format_key_from_date(week_start_date)}"
    dynamodb_client.put_item(
        TableName="MainTable",
        Item={
            "EntityType": {"S": "account#recommendations"},
            "EntityId": {"S": entityId},
            "recommendedMeals": {"L": serialized_meals},
            "expirationDate": {
                "S": (week_start_date + timedelta(days=7)).strftime("%Y-%m-%d")
            },
        },
    )


def create_week_dates(count: int, from_date: date):
    week_dates = [from_date + timedelta(days=x) for x in range(count)]
    return week_dates


def create_recommended_meals(
    current_user_id: str, week_start_date: Optional[date] = None
):
    start_date = week_start_date if week_start_date else date.today()
    start_date = get_start_of_week(start_date)
    week_dates = create_week_dates(7, start_date)
    response = get_raw_current_user_meals(current_user_id)
    if response.get("Count") == 0:
        raise ValueError("No meals found")
    serialized_meals = response.get("Items")
    deserialized_meals = [MealIn(**deserialize_item(meal)) for meal in serialized_meals]
    recommended_meals = randomly_select_meals(deserialized_meals, 7)
    for idx, meal in enumerate(recommended_meals):
        recommended_meals[idx] = MealRecommendationInDB(
            meal=meal,
            date=week_dates[idx].strftime("%Y-%m-%d"),
        )
    return put_recommended_meals(current_user_id, recommended_meals, start_date)


def get_all_recommended_meals(current_user_id: str):
    response = dynamodb_client.query(
        TableName="MainTable",
        FilterExpression="EntityType = :entityType AND begins_with(EntityId, :entityId)",
        ExpressionAttributeValues={
            ":entityType": {"S": "account#recommendations"},
            ":entityId": {"S": current_user_id},
        },
    )
    count = response.get("Count")
    if count == 0:
        return {"meals": [], "userId": current_user_id}
    count = response.get("Count")
    if count == 0:
        return {"meals": [], "userId": current_user_id}
    # TODO : refactor. is currently an array {meals: [MealOut], userId: current_user_id}
    serialized_recommendations = response.get("Items")
    deserialized_recommendations = deserialize_item(serialized_recommendations)
    recommendations = UserMealRecommendations(**deserialized_recommendations)
    return recommendations


def get_raw_recommended_meals(
    current_user_id: str, week_start_date: date
) -> DynamoDBQueryResponse:
    entityId = f"{current_user_id}#{week_start_date}"
    response = dynamodb_client.query(
        TableName="MainTable",
        KeyConditionExpression="EntityType = :entityType AND begins_with(EntityId, :entityId)",
        ExpressionAttributeValues={
            ":entityType": {"S": "account#recommendations"},
            ":entityId": {"S": entityId},
        },
    )

    return response


def get_recommended_meals(current_user_id: str, week_start_date: date):
    response = get_raw_recommended_meals(current_user_id, week_start_date)
    count = response.get("Count")
    if count == 0:
        return UserMealRecommendations(
            userId=current_user_id, mealRecommendations=[], expirationDate=date.today()
        )
    serialized_recommendations = response.get("Items")[0]
    deserialized_recommendations = deserialize_item(serialized_recommendations)
    meal_recommendations = [
        MealRecommendation(**meal)
        for meal in deserialized_recommendations.get("recommendedMeals") or []
    ]
    recommendations = UserMealRecommendations(
        userId=current_user_id,
        mealRecommendations=meal_recommendations,
        expirationDate=deserialized_recommendations.get("expirationDate")
        or date.today(),
    )
    return recommendations
