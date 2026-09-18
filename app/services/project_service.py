from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate


def create_project(
    db: Session,
    project_data: ProjectCreate
):
    user = db.query(User).filter(
        User.id == project_data.user_id
    ).first()

    if user is None:
        return None

    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        user_id=project_data.user_id
    )

    try:
        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        return new_project

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
    query = db.query(Project)

    if name:
        query = query.filter(
            Project.name.ilike(f"%{name}%")
        )

    if user_id:
        query = query.filter(
            Project.user_id == user_id
        )

    if sort_by == "name":
        query = query.order_by(Project.name)

    elif sort_by == "id":
        query = query.order_by(Project.id)

    return query.offset(skip).limit(limit).all()


def get_project(
    db: Session,
    project_id: int
):
    return db.query(Project).filter(
        Project.id == project_id
    ).first()


def update_project(
    db: Session,
    project_id: int,
    name: str,
    description: str
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if project is None:
        return None

    project.name = name
    project.description = description

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project_id: int
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if project is None:
        return False

    db.delete(project)
    db.commit()

    return True