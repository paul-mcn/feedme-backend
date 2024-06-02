from fastapi import FastAPI
from .routers import auth, users, file, meals
from .dependencies.aws import init_db, init_s3

init_db()
init_s3()


app = FastAPI()


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(file.router, prefix="/file", tags=["file"])
app.include_router(meals.router, prefix="/meals", tags=["meals"])


@app.get("/")
async def root():
    return {"Quaid": "Start the Reactor"}
