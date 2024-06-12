from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas import User
from ..dependencies.user import get_current_user
from ..dependencies.meal import get_all_meals

router = APIRouter()


@router.get("")
async def read_all_meals(
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = 20,
    lastEvaluatedKey: str | None = None,
):
    print(limit)
    meals = get_all_meals(limit, lastEvaluatedKey)
    return meals
