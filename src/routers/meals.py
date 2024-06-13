from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas import User
from ..dependencies.user import get_current_user
from ..dependencies.meal import get_all_meals, get_current_user_meals

router = APIRouter()


@router.get("")
async def read_all_meals(
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = 20,
    lastEvaluatedKey: str | None = None,
):
    meals = get_all_meals(limit, lastEvaluatedKey)
    user_meals = get_current_user_meals(current_user.id, limit)
    filtered_meals = []
    for meal in meals.meals:
        if meal.id not in [meal.id for meal in user_meals.meals]:
            filtered_meals.append(meal)
    print(filtered_meals)
    return {"count": len(filtered_meals), "meals": filtered_meals}
