from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v2/users",
    tags=["Users V2"]
)


@router.get("/")
def get_users_v2():
    return {
        "version": "v2",
        "message": "Users API version 2",
        "new_feature": "Improved user response"
    }