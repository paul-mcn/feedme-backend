from typing import Annotated
from fastapi import APIRouter, Depends
from ..schemas import User
from ..dependencies import get_current_user, get_current_active_user


router = APIRouter()

@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/users/me/meals")
async def read_own_meals(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

