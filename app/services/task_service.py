from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from datetime import datetime
from typing import Optional
from fastapi import HTTPException

from app.models.task import Task, StatusEnum, PriorityEnum
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(
    db: Session,
    status: Optional[StatusEnum] = None,
    priority: Optional[PriorityEnum] = None,
    due_before: Optional[datetime] = None,
    sort_by: Optional[str] = "created_at",
    order: Optional[str] = "asc",
) -> list[Task]:
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if due_before:
        query = query.filter(Task.due_date <= due_before)

    sort_column = getattr(Task, sort_by, Task.created_at)
    query = query.order_by(asc(sort_column) if order == "asc" else desc(sort_column))

    return query.all()


def get_task_by_id(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(db: Session, data: TaskCreate) -> Task:
    task = Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate) -> Task:
    task = get_task_by_id(db, task_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = get_task_by_id(db, task_id)
    db.delete(task)
    db.commit()


def update_task_status(db: Session, task_id: int, status: StatusEnum) -> Task:
    task = get_task_by_id(db, task_id)
    task.status = status
    db.commit()
    db.refresh(task)
    return task
