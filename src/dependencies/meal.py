from .aws import deserialize_item, dynamodb_client, serialize_item
from ..types import DynamoDBQueryResponse
from ..schemas import (
    MealCreate,
    MealIn,
    MealOut,
    MealSnapshot,
    UserMeals,
)


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


def get_raw_current_user_meals(current_user_id: str) -> DynamoDBQueryResponse:
    response = dynamodb_client.query(
        TableName="MainTable",
        KeyConditionExpression="EntityType = :entityType AND begins_with(EntityId, :entityId)",
        ExpressionAttributeValues={
            ":entityType": {"S": "account#meals"},
            ":entityId": {"S": current_user_id},
        },
    )
    return response


def get_current_user_meals(current_user_id: str):
    response = get_raw_current_user_meals(current_user_id)
    serialized_meals = response.get("Items")
    count = response.get("Count")
    if count == 0:
        return UserMeals(userId=current_user_id, meals=[])
    deserialized_meals = [
        MealOut(**deserialize_item(meal)) for meal in serialized_meals
    ]
    user_meals = UserMeals(userId=current_user_id, meals=deserialized_meals)
    return user_meals


def create_current_user_meal(current_user_id: str, meal: MealCreate):
    new_meal = MealIn(
        title=meal.title,
        ingredients=meal.ingredients,
        price=meal.price,
        time=meal.time,
        description=meal.description,
        imageURLs=meal.imageURLs,
        snapshotURL=meal.snapshotURL,
        notes=meal.notes
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
