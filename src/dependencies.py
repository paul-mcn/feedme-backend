from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from .schemas import TokenData, User, UserInDB
import boto3
from boto3.dynamodb.types import TypeDeserializer

client = boto3.client("dynamodb")

SECRET_KEY = "c514d86f164e955c01a06db43497aa2a2ce6950b77388259e8bd4916f4134054"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
}

fake_meals_db = [
    {
        "id": "1",
        "name": "Spaghetti",
        "ingredients": ["Pasta", "Tomato Sauce"],
        "description": "Fresh spaghetti with tomato sauce",
        "imageURL": "https://sugarspunrun.com/wp-content/uploads/2023/09/Spaghetti-Meat-Sauce-1-of-1-3.jpg",
        "price": 10.99,
    },
    {
        "id": "2",
        "name": "Lasagna",
        "ingredients": ["Meat", "Cheese", "Tomato Sauce"],
        "description": "Tasty lasagna with meat sauce",
        "imageURL": "https://www.kitchensanctuary.com/wp-content/uploads/2020/10/Lasagne-square-FS-79.jpg",
        "price": 13.99,
    },
]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def dynamodb_to_user(user):
    return {
        "id": user["EntityId"],
        "email": user["EntityId"],
        "firstName": user["FirstName"],
        "lastName": user["LastName"],
        "hashed_password": user["HashedPassword"],
    }


def deserialize_item(item):
    item = {k: TypeDeserializer().deserialize(v) for k, v in item.items()}
    return item


def fake_hash_password(password: str):
    return "fakehashed" + password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(username: str):
    response = client.get_item(
        TableName="MainTable",
        Key={"EntityType": {"S": "account"}, "EntityId": {"S": username}},
    )
    serialized_user = response.get("Item")
    print("serialized_user", serialized_user)
    if serialized_user:
        deserialized_user = deserialize_item(response.get("Item"))
        user = dynamodb_to_user(deserialized_user)
        return UserInDB(**user)


def fake_decode_token(token):
    user = get_user(token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_user_meals(current_user: Annotated[User, Depends(get_current_user)]):
    print("current_user", current_user)
    # response = client.
    # return
