from fastapi import FastAPI

from app.api.routes.users import router as users_router


app = FastAPI(
    title="DevHub API",
    description="Developer platform API built with FastAPI",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to DevHub API"
    }


app.include_router(users_router)