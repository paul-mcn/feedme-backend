from pydantic import BaseModel, ConfigDict, AliasGenerator, field_serializer
from pydantic_settings import SettingsConfigDict, BaseSettings
from urllib.parse import unquote


def to_camel(s):
    return s[0].lower() + s[1:]


model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=to_camel))


class EnvironmentSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env")

class BaseEntity(BaseModel):
    model_config = model_config


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: str
    email: str | None = None
    firstName: str | None = None
    lastName: str | None = None


class UserInDB(User):
    hashed_password: str


class Item(BaseModel):
    name: str
    price: float


class Ingredient(BaseEntity):
    Unit: str
    Value: str
    Title: str


class IngredientGroup(BaseEntity):
    GroupName: str | None
    GroupValues: list[Ingredient]


class Meal(BaseEntity):
    Id: str
    ImageUrl: str
    Title: str
    Price: float
    Ingredients: list[IngredientGroup]

    @field_serializer("ImageUrl")
    def serizlize_image_url(self, value):
        return unquote(value)


class UserMeals(BaseEntity):
    UserId: str
    Meals: list[Meal]
