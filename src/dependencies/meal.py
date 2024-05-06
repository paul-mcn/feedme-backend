from .aws import deserialize_item, dynamodb_client, get_main_db_table, serialize_item
from ..schemas import MealCreate, MealIn, User, UserMeals
from uuid import uuid4


def get_current_user_meals(current_user: User):
    response = dynamodb_client.get_item(
        TableName="MainTable",
        Key={"EntityType": {"S": "account#meals"}, "EntityId": {"S": current_user.id}},
    )
    serialized_meals = response.get("Item")
    if serialized_meals:
        deserialized_meals = deserialize_item(response.get("Item"))
        user_meals = UserMeals(
            userId=deserialized_meals["EntityId"], meals=deserialized_meals["meals"]
        )
        return user_meals
    return {"meals": [], "userId": current_user.id}


def put_current_user_meal(account_id: str, meal: MealCreate):
    uuid = uuid4().hex
    new_meal = MealIn(
        id=uuid,
        title=meal.title,
        ingredients=meal.ingredients,
        price=meal.price,
        time=meal.time,
        description=meal.description,
        imageURLs=meal.imageURLs,
    ).model_dump()
    # print(new_meal)
    serialized_meal = serialize_item(new_meal)
    print(serialized_meal)
    return dynamodb_client.update_item(
        TableName="MainTable",
        Key={"EntityType": {"S": "account#meals"}, "EntityId": {"S": account_id}},
        UpdateExpression="SET meals = list_append(meals, :new_meal)",
        # ExpressionAttributeNames={"#meals": "meals"},
        ExpressionAttributeValues={":new_meal": {"L": [{"M": serialized_meal}]}},
        ReturnValues="ALL_NEW",
    )
