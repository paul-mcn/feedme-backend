from .aws import deserialize_item, dynamodb_client, s3_client
from ..schemas import Meal, User, UserMeals


def dynamodb_to_user_meals(meal):
    return {"UserId": meal["EntityId"], "Meals": meal["Meals"]}


def get_current_user_meals(current_user: User):
    response = dynamodb_client.get_item(
        TableName="MainTable",
        Key={"EntityType": {"S": "account#meals"}, "EntityId": {"S": current_user.id}},
    )
    serialized_meals = response.get("Item")
    if serialized_meals:
        deserialized_meals = deserialize_item(response.get("Item"))
        meals = dynamodb_to_user_meals(deserialized_meals)
        return UserMeals(**meals).model_dump(by_alias=True)
    return {"meals": [], "userId": current_user.id}


def put_current_user_meal(current_user: User, new_meal: Meal):
    dynamodb_client.put_item(
        TableName="MainTable",
        Item={
            "EntityType": {"S": "account#meals"},
            "EntityId": {"S": current_user.id},
            "Meals": {"S": new_meal},
        },
    )

    s3_client.put_object(
        Body=new_meal,
        Bucket="organisemymeals-image-bucket",
        Key=f"{current_user.id}/meals.json",
    )
