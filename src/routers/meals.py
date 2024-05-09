from typing import Annotated
from fastapi import APIRouter, Depends
from ..dependencies.user import oauth2_scheme

router = APIRouter()


@router.get("")
async def read_meals(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"meals": [], "uhhh bro": "what the frick"}


# @router.get("/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @router.put("/item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}