from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str
    user_id: int


class ProjectUpdate(BaseModel):
    name: str
    description: str


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int