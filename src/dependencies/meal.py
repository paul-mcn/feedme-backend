from .aws import deserialize_item, dynamodb_client
from ..schemas import User, UserMeals



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
