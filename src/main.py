from fastapi import FastAPI
from .routers import auth, users, file
from .dependencies.aws import init_db, init_s3

init_db()
init_s3()


app = FastAPI()


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(file.router, prefix="/file", tags=["file"])


@app.get("/")
async def root():
    return {"Quaid": "Start the Reactor"}
