import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# --- Helpers ---

def create_sample_task(**kwargs):
    payload = {"title": "Test Task", "priority": "medium", **kwargs}
    return client.post("/api/v1/tasks", json=payload)


# --- CRUD ---

def test_create_task():
    res = create_sample_task(description="desc", priority="high", due_date="2025-12-31T00:00:00")
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "todo"
    assert data["priority"] == "high"


def test_get_all_tasks():
    create_sample_task()
    create_sample_task(title="Task 2")
    res = client.get("/api/v1/tasks")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_task_by_id():
    task_id = create_sample_task().json()["id"]
    res = client.get(f"/api/v1/tasks/{task_id}")
    assert res.status_code == 200
    assert res.json()["id"] == task_id


def test_update_task():
    task_id = create_sample_task().json()["id"]
    res = client.put(f"/api/v1/tasks/{task_id}", json={"title": "Updated", "priority": "low"})
    assert res.status_code == 200
    assert res.json()["title"] == "Updated"
    assert res.json()["priority"] == "low"


def test_delete_task():
    task_id = create_sample_task().json()["id"]
    res = client.delete(f"/api/v1/tasks/{task_id}")
    assert res.status_code == 204
    assert client.get(f"/api/v1/tasks/{task_id}").status_code == 404


def test_update_status():
    task_id = create_sample_task().json()["id"]
    res = client.patch(f"/api/v1/tasks/{task_id}/status", json={"status": "in_progress"})
    assert res.status_code == 200
    assert res.json()["status"] == "in_progress"


# --- 404 ---

def test_get_task_not_found():
    assert client.get("/api/v1/tasks/999").status_code == 404


def test_update_task_not_found():
    assert client.put("/api/v1/tasks/999", json={"title": "x"}).status_code == 404


def test_delete_task_not_found():
    assert client.delete("/api/v1/tasks/999").status_code == 404


def test_update_status_not_found():
    assert client.patch("/api/v1/tasks/999/status", json={"status": "done"}).status_code == 404


# --- Filter & Sort ---

def test_filter_by_status():
    task_id = create_sample_task().json()["id"]
    client.patch(f"/api/v1/tasks/{task_id}/status", json={"status": "done"})
    create_sample_task(title="Todo Task")

    res = client.get("/api/v1/tasks?status=done")
    assert all(t["status"] == "done" for t in res.json())


def test_filter_by_priority():
    create_sample_task(priority="high")
    create_sample_task(priority="low")

    res = client.get("/api/v1/tasks?priority=high")
    assert all(t["priority"] == "high" for t in res.json())


def test_filter_due_before():
    create_sample_task(due_date="2025-01-01T00:00:00")
    create_sample_task(due_date="2026-01-01T00:00:00")

    res = client.get("/api/v1/tasks?due_before=2025-06-01T00:00:00")
    assert len(res.json()) == 1


def test_sort_order():
    create_sample_task(title="A Task", priority="low")
    create_sample_task(title="B Task", priority="high")

    res = client.get("/api/v1/tasks?sort_by=title&order=desc")
    titles = [t["title"] for t in res.json()]
    assert titles == sorted(titles, reverse=True)


# --- Validation ---

def test_create_task_missing_title():
    res = client.post("/api/v1/tasks", json={"priority": "high"})
    assert res.status_code == 422


def test_update_status_invalid_value():
    task_id = create_sample_task().json()["id"]
    res = client.patch(f"/api/v1/tasks/{task_id}/status", json={"status": "invalid_status"})
    assert res.status_code == 422
