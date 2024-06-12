from typing import Annotated
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import botocore.exceptions

from ..dependencies.env import get_environment_settings
from .aws import deserialize_item, dynamodb_client
from ..schemas import TokenData, UserInDB
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

env_settings = get_environment_settings()


def fake_hash_password(password: str):
    return "fakehashed" + password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user_by_email(username)
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
    encoded_jwt = jwt.encode(
        to_encode, env_settings.SECRET_KEY, algorithm=env_settings.ALGORITHM
    )
    return encoded_jwt


def put_user(email: str, password: str):
    id = uuid.uuid4().hex
    hashed_password = get_password_hash(password)
    dynamodb_client.put_item(
        TableName="MainTable",
        Item={
            "EntityType": {"S": "account"},
            "EntityId": {"S": id},
            "email": {"S": email},
            "firstName": {"NULL": True},
            "lastName": {"NULL": True},
            "hashedPassword": {"S": hashed_password},
        },
        ConditionExpression="attribute_not_exists(EntityId)",
    )
    return id


def get_user_by_email(email: str):
    response = dynamodb_client.query(
        TableName="MainTable",
        IndexName="EntityType-email-index",
        KeyConditionExpression="EntityType = :entityType AND email = :email",
        ExpressionAttributeValues={
            ":entityType": {"S": "account"},
            ":email": {"S": email},
        },
    )
    serialized_users = response.get("Items")
    count = response.get("Count")
    serialized_user = serialized_users[0] if count > 0 else None
    if serialized_user:
        deserialized_user = deserialize_item(serialized_user)
        user = UserInDB(**deserialized_user)
        return user


def get_user_by_id(id: str):
    response = dynamodb_client.get_item(
        TableName="MainTable",
        Key={"EntityType": {"S": "account"}, "EntityId": {"S": id}},
    )
    serialized_user = response.get("Item")
    if serialized_user:
        deserialized_user = deserialize_item(response.get("Item"))
        return UserInDB(**deserialized_user)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, env_settings.SECRET_KEY, algorithms=[env_settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(id=token_data.username)
    if user is None:
        raise credentials_exception
    return user
