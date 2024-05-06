from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, AliasGenerator, field_serializer
from .dependencies.aws import s3_client
from .dependencies.env import get_environment_settings

settings = get_environment_settings()


def to_camel(s):
    return s[0].lower() + s[1:]


model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=to_camel))


class BaseEntity(BaseModel):
    model_config = model_config


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ImageURL(BaseEntity):
    id: str


class User(BaseModel):
    id: str
    email: str | None = None
    firstName: str | None = None
    lastName: str | None = None


class UserInDB(User):
    hashed_password: str


class Item(BaseModel):
    name: str
    price: Decimal


class Ingredient(BaseEntity):
    unit: str | None
    value: str
    title: str | None


class IngredientGroup(BaseEntity):
    groupName: str | None
    groupValues: list[Ingredient]


class MealIn(BaseEntity):
    id: str
    title: str
    price: Decimal | None
    ingredients: str | None
    time: Optional[int] = None
    description: Optional[str] = None
    imageURLs: list[ImageURL]


class MealOut(MealIn):
    @field_serializer("imageURLs", check_fields=False)
    def serizlize_image_url(self, imageURLs: list[ImageURL]):
        for imageURL in imageURLs:
            try:
                imageURL.id = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": imageURL.id},
                )
            except Exception as e:
                print(e)
                imageURL.id = ""

        return imageURLs

class MealCreate(BaseEntity):
    title: str
    price: Decimal | None
    ingredients: str | None
    time: Optional[int] = None
    description: Optional[str] = None
    imageURLs: list[ImageURL]

class UserMeals(BaseEntity):
    userId: str
    meals: list[MealOut]
