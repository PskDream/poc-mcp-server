# Todo Management Backend — POC

Backend REST API สำหรับระบบจัดการ Todo ที่สร้างด้วย **Python + FastAPI** และ **SQLite**

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Framework | FastAPI |
| Database | SQLite (via SQLAlchemy 2.0) |
| Migration | Alembic |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Testing | Pytest + httpx |

---

## Project Structure

```
app/
├── main.py              # FastAPI app entry point
├── database.py          # SQLAlchemy engine + session + Base
├── models/task.py       # ORM model (Task, StatusEnum, PriorityEnum)
├── schemas/task.py      # Pydantic schemas (Create, Update, StatusUpdate, Response)
├── routers/tasks.py     # Route definitions
└── services/task_service.py  # Business logic
tests/
└── test_tasks.py        # 16 tests covering CRUD, filter, sort, validation
alembic/                 # Database migrations
```

---

## Getting Started

```bash
# 1. สร้าง virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. ติดตั้ง dependencies
pip install -r requirements.txt

# 3. ตั้งค่า environment
cp .env.example .env

# 4. รัน migration
alembic upgrade head

# 5. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server: `http://localhost:8000`
Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

---

## API Endpoints

Base path: `/api/v1/tasks`

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | ดึงรายการ Task ทั้งหมด |
| `POST` | `/` | สร้าง Task ใหม่ (201) |
| `GET` | `/{id}` | ดึง Task ตาม ID |
| `PUT` | `/{id}` | แก้ไข Task |
| `DELETE` | `/{id}` | ลบ Task (204) |
| `PATCH` | `/{id}/status` | อัปเดตเฉพาะ status |

### Query Parameters — GET /api/v1/tasks

| Parameter | Type | Description |
|---|---|---|
| `status` | `todo` \| `in_progress` \| `done` | กรองตามสถานะ |
| `priority` | `low` \| `medium` \| `high` | กรองตาม priority |
| `due_before` | datetime | Task ที่ครบกำหนดก่อนวันที่ระบุ |
| `sort_by` | string | field ที่ใช้เรียง (default: `created_at`) |
| `order` | `asc` \| `desc` | ทิศทางการเรียง (default: `asc`) |

---

## Running Tests

```bash
# รัน test ทั้งหมด
pytest

# รันพร้อม coverage
pytest --cov=app --cov-report=term-missing

# รัน test เฉพาะ file
pytest tests/test_tasks.py -v
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./todo.db` | SQLAlchemy connection string |
| `APP_ENV` | `development` | Environment name |
| `DEBUG` | `true` | Debug mode |

---

## MCP Server

`app/mcp_server.py` expose ทุก operation ของ Todo เป็น MCP tools สำหรับใช้กับ AI agents

### Tools

| Tool | Description |
|---|---|
| `list_tasks` | ดึงรายการ task พร้อม filter/sort |
| `get_task` | ดึง task ตาม `task_id` |
| `create_task` | สร้าง task ใหม่ |
| `update_task` | แก้ไข task (ทุก field optional) |
| `update_task_status` | อัปเดตเฉพาะ status |
| `delete_task` | ลบ task |

### Endpoint

MCP server รันรวมกับ FastAPI บน port เดียวกัน:

```
POST http://localhost:8000/mcp
```

### Client Config (Claude Desktop)

```json
{
  "mcpServers": {
    "todo": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Run MCP Inspector (dev)

```bash
mcp dev app/mcp_server.py
```

เปิด browser ที่ URL ที่แสดงใน terminal แล้วตั้งค่า:
- **Command:** `.venv/bin/python`
- **Arguments:** `app/mcp_server.py`

---

## Roadmap (หลัง POC)

- [ ] Authentication (JWT)
- [ ] User Management & Multi-tenant
- [ ] Categories / Tags
- [ ] Migrate SQLite → PostgreSQL
- [ ] Docker & Docker Compose
- [ ] CI/CD Pipeline
