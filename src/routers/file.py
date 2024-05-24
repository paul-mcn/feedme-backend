from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies.user import get_current_user
from ..schemas import User
from ..dependencies.file import get_presigned_post


router = APIRouter()


@router.get("/image-upload")
async def upload_image(current_user: Annotated[User, Depends(get_current_user)]):
    response = get_presigned_post()

    if response is None:
        raise HTTPException(status_code=409, detail="Could not upload image")

    return response
