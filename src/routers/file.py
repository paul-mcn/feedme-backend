from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies.user import get_current_user
from ..schemas import User
from ..dependencies.file import upload_new_image


router = APIRouter()


@router.get("/image-upload")
async def upload_image(current_user: Annotated[User, Depends(get_current_user)]):
    response = upload_new_image()

    if response is None:
        raise HTTPException(status_code=409, detail="Could not upload image")

    return response
