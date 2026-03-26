from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.task import StatusEnum, PriorityEnum
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    status: Optional[StatusEnum] = Query(None),
    priority: Optional[PriorityEnum] = Query(None),
    due_before: Optional[datetime] = Query(None),
    sort_by: Optional[str] = Query("created_at"),
    order: Optional[str] = Query("asc"),
    db: Session = Depends(get_db),
):
    return task_service.get_tasks(db, status, priority, due_before, sort_by, order)


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, data)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task_by_id(db, task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, data)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service.delete_task(db, task_id)


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_status(task_id: int, data: TaskStatusUpdate, db: Session = Depends(get_db)):
    return task_service.update_task_status(db, task_id, data.status)
