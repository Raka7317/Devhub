from sqlalchemy.orm import Session

from app.models.project import Project


def create(
    db: Session,
    project: Project
):
    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_by_id(
    db: Session,
    project_id: int
):
    return db.query(Project).filter(
        Project.id == project_id
    ).first()


def get_all(
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


def update(
    db: Session,
    project: Project
):
    db.commit()
    db.refresh(project)

    return project


def delete(
    db: Session,
    project: Project
):
    db.delete(project)
    db.commit()