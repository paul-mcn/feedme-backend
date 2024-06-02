from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from src.dependencies.file import upload_image_from_path
from src.dependencies.meal import create_current_user_meal, get_current_user_meals
from src.dependencies.env import get_environment_settings
from ..schemas import MealCreate, User
from ..dependencies.user import get_current_user
from .user_meals import router as meals_router
from ..default_meals import meals

settings = get_environment_settings()

router = APIRouter()

router.include_router(meals_router, prefix="/me/meals", tags=["meals"])


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return User(
        id=current_user.id,
        email=current_user.email,
        firstName=current_user.firstName,
        lastName=current_user.lastName,
    )


@router.post("/me/setup-account")
async def setup_account(current_user: Annotated[User, Depends(get_current_user)]):
    user_meals = get_current_user_meals(current_user.id, limit=1)
    if len(user_meals.meals) > 0:
        return current_user
    for meal in meals:
        imageURLs = []
        for image in meal.get("imageURLs") or []:
            try:
                image_path = Path(
                    settings.PROJECT_ROOT,
                    "src",
                    "assets",
                    "images",
                    "default_meals",
                    image.get("filename"),
                )
                image_id = upload_image_from_path(image_path)
                imageURLs.append({"id": image_id})
            except Exception as e:
                raise e
        created_meal = MealCreate(
            title=meal.get("title") or "",
            ingredients=meal.get("ingredients"),
            price=meal.get("price"),
            time=meal.get("time"),
            description=meal.get("description"),
            imageURLs=imageURLs,
            snapshotURL=meal.get("snapshotURL"),
            notes=meal.get("notes"),
        )
        create_current_user_meal(current_user.id, created_meal)
    return current_user
