from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    age: int


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int