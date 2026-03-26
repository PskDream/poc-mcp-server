import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.task import StatusEnum, PriorityEnum
from app.schemas.task import TaskCreate, TaskUpdate
from app.services import task_service

mcp = FastMCP("Todo Management", stateless_http=True, streamable_http_path="/")


def _db():
    return next(get_db())


@mcp.tool()
def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_before: Optional[str] = None,
    sort_by: str = "created_at",
    order: str = "asc",
) -> list[dict]:
    """List all tasks with optional filters and sorting."""
    db = _db()
    tasks = task_service.get_tasks(
        db,
        status=StatusEnum(status) if status else None,
        priority=PriorityEnum(priority) if priority else None,
        due_before=datetime.fromisoformat(due_before) if due_before else None,
        sort_by=sort_by,
        order=order,
    )
    return [_task_to_dict(t) for t in tasks]


@mcp.tool()
def get_task(task_id: int) -> dict:
    """Get a task by ID."""
    db = _db()
    return _task_to_dict(task_service.get_task_by_id(db, task_id))


@mcp.tool()
def create_task(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
) -> dict:
    """Create a new task."""
    db = _db()
    data = TaskCreate(
        title=title,
        description=description,
        priority=PriorityEnum(priority),
        due_date=datetime.fromisoformat(due_date) if due_date else None,
    )
    return _task_to_dict(task_service.create_task(db, data))


@mcp.tool()
def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
) -> dict:
    """Update a task. Only provided fields will be changed."""
    db = _db()
    data = TaskUpdate(
        title=title,
        description=description,
        status=StatusEnum(status) if status else None,
        priority=PriorityEnum(priority) if priority else None,
        due_date=datetime.fromisoformat(due_date) if due_date else None,
    )
    return _task_to_dict(task_service.update_task(db, task_id, data))


@mcp.tool()
def delete_task(task_id: int) -> dict:
    """Delete a task by ID."""
    db = _db()
    task_service.delete_task(db, task_id)
    return {"deleted": True, "task_id": task_id}


@mcp.tool()
def update_task_status(task_id: int, status: str) -> dict:
    """Update only the status of a task. status: todo | in_progress | done"""
    db = _db()
    return _task_to_dict(task_service.update_task_status(db, task_id, StatusEnum(status)))


def _task_to_dict(task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
