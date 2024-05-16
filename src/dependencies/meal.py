from datetime import date, datetime, timedelta
import random
from .aws import deserialize_item, dynamodb_client, serialize_item
from ..schemas import (
    MealBase,
    MealCreate,
    MealIn,
    MealOut,
    MealSnapshot,
    UserMealRecommendations,
    UserMeals,
    MealRecommendation,
)


def create_meal_recommendations(meals: list, count: int):
    randomly_selected_meals = random.sample(meals, min(count, 7))
    return randomly_selected_meals


def create_week_dates(count: int):
    week_dates = [date.today() + timedelta(days=x) for x in range(count)]
    return week_dates


def get_meal_snapshot(encodedUrl: str):
    response = dynamodb_client.get_item(
        TableName="MainTable",
        Key={
            "EntityType": {"S": "meal#web-page-snapshot"},
            "EntityId": {"S": encodedUrl},
        },
    )
    serialized_meal = response.get("Item")
    if serialized_meal:
        deserialized_meal = deserialize_item(serialized_meal)
        return MealSnapshot(**deserialized_meal)


def get_meal_recommendations(current_user_id: str):
    response = dynamodb_client.query(
        TableName="MainTable",
        KeyConditionExpression="EntityType = :entityType AND begins_with(EntityId, :entityId)",
        ExpressionAttributeValues={
            ":entityType": {"S": "account#meals"},
            ":entityId": {"S": current_user_id},
        },
    )
    serialized_meals = response.get("Items")
    count = response.get("Count")
    if count == 0:
        return {"mealRecommendations": [], "userId": current_user_id}
    # this happens before deserialization to save on processing time
    randomly_selected_meals = create_meal_recommendations(serialized_meals, count)
    week_dates = create_week_dates(count)
    print(week_dates)
    deserialized_meals = [
        MealRecommendation(meal=MealOut(**deserialize_item(meal)), date=date.today())
        for meal in randomly_selected_meals
    ]
    user_meals = UserMealRecommendations(
        userId=current_user_id, mealRecommendations=deserialized_meals
    )
    return user_meals


def get_current_user_meals(current_user_id: str):
    response = dynamodb_client.query(
        TableName="MainTable",
        KeyConditionExpression="EntityType = :entityType AND begins_with(EntityId, :entityId)",
        ExpressionAttributeValues={
            ":entityType": {"S": "account#meals"},
            ":entityId": {"S": current_user_id},
        },
    )
    serialized_meals = response.get("Items")
    count = response.get("Count")
    if count == 0:
        return {"meals": [], "userId": current_user_id}
    deserialized_meals = [
        MealOut(**deserialize_item(meal)) for meal in serialized_meals
    ]
    user_meals = UserMeals(userId=current_user_id, meals=deserialized_meals)
    return user_meals


def create_current_user_meal(current_user_id: str, meal: MealBase):
    new_meal = MealIn(
        title=meal.title,
        ingredients=meal.ingredients,
        price=meal.price,
        time=meal.time,
        description=meal.description,
        imageURLs=meal.imageURLs,
        snapshotURL=meal.snapshotURL,
    ).model_dump()
    serialized_meal = serialize_item(new_meal)
    return dynamodb_client.put_item(
        TableName="MainTable",
        Item={
            "EntityType": {"S": "account#meals"},
            "EntityId": {"S": f"{current_user_id}#{new_meal['mealId']}"},
            **serialized_meal,
        },
    )
