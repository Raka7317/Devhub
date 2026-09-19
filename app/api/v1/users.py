from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users V1"]
)


@router.get("/")
def get_users_v1():
    return {
        "version": "v1",
        "message": "Users API version 1"
    }