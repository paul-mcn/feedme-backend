from fastapi import FastAPI
from .routers import meals, auth, users


app = FastAPI()

app.include_router(meals.router, prefix="/meals", tags=["meals"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
