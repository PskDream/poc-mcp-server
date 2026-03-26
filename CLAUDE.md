# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Todo Management Backend POC — a REST API for task management built with Python + FastAPI and SQLite. This is a proof-of-concept; the planned post-POC migration path is SQLite → PostgreSQL.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
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
├── main.py                  # FastAPI app entry point + lifespan (DB init + MCP session)
├── database.py              # SQLAlchemy engine + session setup
├── models/task.py           # SQLAlchemy ORM model (StatusEnum, PriorityEnum)
├── schemas/task.py          # Pydantic v2 request/response schemas
├── routers/tasks.py         # Route definitions for /api/v1/tasks
├── services/task_service.py # Business logic layer
└── mcp_server.py            # MCP server (Streamable HTTP), mounted at /mcp
```

Layered architecture: routers and MCP tools both call `task_service.py` — no duplicate logic. Pydantic schemas are used for input validation and response serialization (separate from ORM models).

MCP server uses `stateless_http=True` and is mounted as a sub-app on FastAPI via `app.mount("/mcp", mcp.streamable_http_app())`. The MCP session manager is started inside FastAPI's lifespan.

## Data Model

`Task` fields: `id`, `title` (required), `description`, `status` (`todo`/`in_progress`/`done`), `priority` (`low`/`medium`/`high`), `due_date`, `created_at`, `updated_at`.

## API

All task endpoints under `/api/v1/tasks`. `GET /api/v1/tasks` supports query params: `status`, `priority`, `due_before`, `sort_by`, `order`.

Status can be updated independently via `PATCH /api/v1/tasks/{id}/status`.

## MCP Server

MCP endpoint: `http://localhost:8000/mcp` (Streamable HTTP transport, stateless)

Tools: `list_tasks`, `get_task`, `create_task`, `update_task`, `update_task_status`, `delete_task`

Dev/inspect:
```bash
mcp dev app/mcp_server.py
# In Inspector UI: Command=.venv/bin/python, Args=app/mcp_server.py
```

## TODO
View todos in [TODO.md](TODO.md), after tasks are completed pls checked mark them.