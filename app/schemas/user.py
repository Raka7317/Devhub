from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.project import ProjectSimpleResponse


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    password: str


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    age: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int


class UserWithProjectsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    projects: list[ProjectSimpleResponse]