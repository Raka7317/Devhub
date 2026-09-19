from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import pagination_params
from app.api.deps import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectSimpleResponse,
    ProjectWithOwnerResponse
)
from app.services import project_service
router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = project_service.create_project(
        db,
        project
    )

    if new_project is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return new_project


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    name: str | None = None,
    user_id: int | None = None,
    sort_by: str = "id",
    db: Session = Depends(get_db)
):
    return project_service.get_projects(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        user_id=user_id,
        sort_by=sort_by
    )



@router.get(
    "/with-owners",
    response_model=list[ProjectWithOwnerResponse]
)
def get_projects_with_owners(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Project.id,
            Project.name,
            Project.description,
            Project.user_id,
            User.name.label("owner_name"),
            User.email.label("owner_email")
        )
        .join(
            User,
            Project.user_id == User.id
        )
        .all()
    )

    return results


@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = project_service.get_project(
        db,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project

@router.put(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    project = project_service.update_project(
        db=db,
        project_id=project_id,
        name=project_data.name,
        description=project_data.description
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    deleted = project_service.delete_project(
        db,
        project_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "message": "Project deleted successfully"
    }

@router.get("/paginated")
def get_paginated_projects(
    pagination: dict = Depends(pagination_params),
    db: Session = Depends(get_db)
):
    projects = (
        db.query(Project)
        .offset(pagination["skip"])
        .limit(pagination["limit"])
        .all()
    )

    return projects