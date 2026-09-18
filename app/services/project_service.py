from sqlalchemy.orm import Session

from app.models.project import Project

from app.schemas.project import ProjectCreate

from app.repositories import (
    project_repository,
    user_repository
)

def create_project(
    db: Session,
    project_data: ProjectCreate
):
    user = user_repository.get_by_id(
    db,
    project_data.user_id
)

    if user is None:
        return None

    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        user_id=project_data.user_id
    )

    try:
        return project_repository.create(
            db,
            new_project
        )

    except Exception:
        db.rollback()
        raise


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    user_id: int | None = None,
    sort_by: str = "id"
):
    return project_repository.get_all(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        user_id=user_id,
        sort_by=sort_by
    )


def get_project(
    db: Session,
    project_id: int
):
    return project_repository.get_by_id(
        db,
        project_id
    )


def update_project(
    db: Session,
    project_id: int,
    name: str,
    description: str
):
    project = project_repository.get_by_id(
        db,
        project_id
    )

    if project is None:
        return None

    project.name = name
    project.description = description

    return project_repository.update(
        db,
        project
    )


def delete_project(
    db: Session,
    project_id: int
):
    project = project_repository.get_by_id(
        db,
        project_id
    )

    if project is None:
        return False

    project_repository.delete(
        db,
        project
    )

    return True