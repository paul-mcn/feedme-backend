from datetime import datetime, timezone
from .aws import deserialize_item, dynamodb_client, serialize_item
from ..types import DynamoDBQueryResponse
from ..schemas import (
    MealIn,
    MealOut,
    MealQueryResponse,
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


def get_raw_current_user_meals(
    current_user_id: str, limit: int
) -> DynamoDBQueryResponse:
    response = dynamodb_client.query(
        TableName="MainTable",
        KeyConditionExpression="EntityType = :entityType AND begins_with(EntityId, :entityId)",
        ExpressionAttributeValues={
            ":entityType": {"S": "account#meals"},
            ":entityId": {"S": current_user_id},
        },
        Limit=limit,
    )
    return response


def get_raw_all_meals(
    limit: int = 20, lastEvaluatedKey: str | None = None
) -> DynamoDBQueryResponse:
    args = {"Limit": limit, "LastEvaluatedKey": lastEvaluatedKey}
    args = {key: value for key, value in args.items() if value is not None}
    response = dynamodb_client.query(
        TableName="MainTable",
        KeyConditionExpression="EntityType = :entityType",
        ExpressionAttributeValues={
            ":entityType": {"S": "all#meals"},
        },
        **args,
    )
    return response


def get_all_meals(limit: int = 20, lastEvaluatedKey: str | None = None):
    response = get_raw_all_meals(limit=limit, lastEvaluatedKey=lastEvaluatedKey)
    serialized_meals = response.get("Items")
    count = response.get("Count")
    if count == 0:
        return MealQueryResponse(count=0, meals=[])
    deserialized_meals = [
        MealOut(**deserialize_item(meal)) for meal in serialized_meals
    ]
    return MealQueryResponse(count=count, meals=deserialized_meals)


def get_current_user_meals(current_user_id: str, limit: int = 20):
    response = get_raw_current_user_meals(current_user_id, limit)
    serialized_meals = response.get("Items")
    count = response.get("Count")
    if count == 0:
        return UserMeals(userId=current_user_id, meals=[])
    deserialized_meals = [
        MealOut(**deserialize_item(meal)) for meal in serialized_meals
    ]
    user_meals = UserMeals(userId=current_user_id, meals=deserialized_meals)
    return user_meals


def create_current_user_meal(current_user_id: str, meal: MealIn):
    meal.follows = meal.follows + 1
    new_meal = meal.model_dump()
    serialized_meal = serialize_item(new_meal)
    dynamodb_client.put_item(
        TableName="MainTable",
        Item={
            "EntityType": {"S": "account#meals"},
            "EntityId": {"S": f"{current_user_id}#{new_meal['mealId']}"},
        },
    )
    dynamodb_client.put_item(
        TableName="MainTable",
        Item={
            "EntityType": {"S": "all#meals"},
            "EntityId": {"S": new_meal["mealId"]},
            **serialized_meal,
            "createdAt": {"S": datetime.now(timezone.utc).isoformat()},
            "updatedAt": {"S": datetime.now(timezone.utc).isoformat()},
        },
    )


def follow_meal(current_user_id: str, meal_id: str):
    dynamodb_client.update_item(
        TableName="MainTable",
        Key={
            "EntityType": {"S": "all#meals"},
            "EntityId": {"S": meal_id},
        },
        UpdateExpression="ADD follows :inc",
        ExpressionAttributeValues={":inc": {"N": "1"}},
        ConditionExpression="attribute_not_exists(EntityId)",
    )
    dynamodb_client.put_item(
        TableName="MainTable",
        Item={
            "EntityType": {"S": "account#meals"},
            "EntityId": {"S": f"{current_user_id}#{meal_id}"},
        },
    )


def batch_follow_meals(current_user_id: str, meal_ids: list[str]):
    for meal_id in meal_ids:
        follow_meal(current_user_id, meal_id)
