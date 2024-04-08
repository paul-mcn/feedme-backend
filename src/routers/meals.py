from typing import Annotated
from fastapi import APIRouter, Depends

router = APIRouter(
)

fake_meals_db = [
    {
        "name": "Spaghetti",
        "price": 10.99,
    },
    {
        "name": "Lasagna",
        "price": 13.99,
    },
]


@router.get("")
async def read_meals():
# async def read_meals(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": "token", "meals": fake_meals_db}


# @router.get("/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @router.put("/item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

