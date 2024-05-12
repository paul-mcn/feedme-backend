from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..dependencies.user import (
    authenticate_user,
    create_access_token,
    get_user,
    create_user,
    get_user_by_email,
)
from ..schemas import Token
from ..dependencies.env import get_environment_settings


router = APIRouter(responses={404: {"description": "Not found"}})

env_settings = get_environment_settings()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=env_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = get_user_by_email(email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        new_user = create_user(email, password)
    except Exception as e:
        raise e
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Something went wrong",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return new_user
