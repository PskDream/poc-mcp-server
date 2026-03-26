# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Todo Management Backend POC — a REST API for task management built with Python + FastAPI and SQLite. This is a proof-of-concept; the planned post-POC migration path is SQLite → PostgreSQL.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
```

`.env` variables: `DATABASE_URL`, `APP_ENV`, `DEBUG`

## Commands

```bash
# Run dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Run a single test file
pytest tests/test_tasks.py -v

# Run database migrations
alembic upgrade head
```

API docs auto-generated at `http://localhost:8000/docs` (Swagger) and `/redoc`.

## Architecture

```
app/
├── main.py           # FastAPI app entry point
├── database.py       # SQLAlchemy engine + session setup
├── models/task.py    # SQLAlchemy ORM model
├── schemas/task.py   # Pydantic v2 request/response schemas
├── routers/tasks.py  # Route definitions for /api/v1/tasks
└── services/task_service.py  # Business logic layer
```

Layered architecture: routers call services, services interact with the database via SQLAlchemy ORM models. Pydantic schemas are used for input validation and response serialization (separate from ORM models).

## Data Model

`Task` fields: `id`, `title` (required), `description`, `status` (`todo`/`in_progress`/`done`), `priority` (`low`/`medium`/`high`), `due_date`, `created_at`, `updated_at`.

## API

All task endpoints under `/api/v1/tasks`. `GET /api/v1/tasks` supports query params: `status`, `priority`, `due_before`, `sort_by`, `order`.

Status can be updated independently via `PATCH /api/v1/tasks/{id}/status`.

## TODO
View todos in [TODO.md](TODO.md), after tasks are completed pls checked mark them.