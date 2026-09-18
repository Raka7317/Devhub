from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.project import ProjectSimpleResponse


class UserCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50
    )

    email: EmailStr

    age: int = Field(
        ge=13,
        le=100
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserUpdate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50
    )

    email: EmailStr

    age: int = Field(
        ge=13,
        le=100
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    role: str


class UserWithProjectsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    role: str
    projects: list[ProjectSimpleResponse]