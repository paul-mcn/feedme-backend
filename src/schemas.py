from pydantic import BaseModel

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


