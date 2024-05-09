import random
from .aws import deserialize_item, dynamodb_client, serialize_item
from ..schemas import MealCreate, MealIn, MealOut, UserMealRecommendations, UserMeals


def create_meal_recommendations(meals: list):
    randomly_selected_meals = random.sample(meals, 3)
    return randomly_selected_meals


def get_meal_recommendations(current_user_id: str):
    response = dynamodb_client.query(
        TableName="MainTable",
        IndexName="EntityType-title-index",
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
    randomly_selected_meals = create_meal_recommendations(serialized_meals)
    deserialized_meals = [
        MealOut(**deserialize_item(meal)) for meal in randomly_selected_meals
    ]
    user_meals = UserMealRecommendations(userId=current_user_id, mealRecommendations=deserialized_meals)
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


def create_current_user_meal(current_user_id: str, meal: MealCreate):

    # TODO: web scrape url to get ingredients, title, and other info
    # for automatic form filling
    new_meal = MealIn(
        title=meal.title,
        ingredients=meal.ingredients,
        price=meal.price,
        time=meal.time,
        description=meal.description,
        imageURLs=meal.imageURLs,
    ).model_dump()

    serialized_meal = serialize_item(new_meal)
    print(serialized_meal)

    return dynamodb_client.put_item(
        TableName="MainTable",
        Item={
            "EntityType": {"S": "account#meals"},
            "EntityId": {"S": f"{current_user_id}#{new_meal['mealId']}"},
            **serialized_meal,
        },
    )


def put_current_user_meal(account_id: str, meal: MealCreate):
    new_meal = MealIn(
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