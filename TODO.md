# TODO — Todo Management Backend POC

## Phase 1: Project Setup

- [x] สร้างไฟล์ `requirements.txt`
- [x] สร้างไฟล์ `.env.example`
- [x] สร้างไฟล์ `.gitignore` (เพิ่ม `venv/`, `*.db`, `.env`)
- [x] สร้างโครงสร้างโฟลเดอร์ `app/` และ `tests/`

## Phase 2: Database & Models

- [x] สร้าง `app/database.py` — SQLAlchemy engine + session + Base
- [x] สร้าง `app/models/task.py` — ORM model สำหรับ Task
- [x] ตั้งค่า Alembic (`alembic init alembic`)
- [x] สร้าง migration แรก (`alembic revision --autogenerate -m "create tasks table"`)
- [x] ทดสอบ `alembic upgrade head` รันได้สำเร็จ

## Phase 3: Schemas

- [x] สร้าง `app/schemas/task.py`
- [x] `TaskCreate` — input schema สำหรับ POST
- [x] `TaskUpdate` — input schema สำหรับ PUT
- [x] `TaskStatusUpdate` — input schema สำหรับ PATCH status
- [x] `TaskResponse` — output schema

## Phase 4: Service Layer

- [x] สร้าง `app/services/task_service.py`
- [x] `get_tasks(filters, sort)` — ดึง task ทั้งหมด พร้อม filter/sort
- [x] `get_task_by_id(id)` — ดึง task ตาม ID
- [x] `create_task(data)` — สร้าง task ใหม่
- [x] `update_task(id, data)` — แก้ไข task
- [x] `delete_task(id)` — ลบ task
- [x] `update_task_status(id, status)` — อัปเดตเฉพาะ status

## Phase 5: Routers

- [x] สร้าง `app/routers/tasks.py`
- [x] `GET /api/v1/tasks` — พร้อม query params (`status`, `priority`, `due_before`, `sort_by`, `order`)
- [x] `POST /api/v1/tasks` — สร้าง task ใหม่ (return 201)
- [x] `GET /api/v1/tasks/{id}` — ดึง task ตาม ID (return 404 ถ้าไม่พบ)
- [x] `PUT /api/v1/tasks/{id}` — แก้ไข task
- [x] `DELETE /api/v1/tasks/{id}` — ลบ task (return 204)
- [x] `PATCH /api/v1/tasks/{id}/status` — อัปเดต status

## Phase 6: App Entry Point

- [x] สร้าง `app/main.py` — สร้าง FastAPI instance, register router, lifespan

## Phase 7: Tests

- [x] สร้าง `tests/test_tasks.py`
- [x] Test CRUD ครบทุก endpoint
- [x] Test filter และ sort ใน GET /tasks
- [x] Test 404 เมื่อ task ไม่มีอยู่
- [x] Test validation error (ส่ง data ไม่ครบ)
- [x] Test PATCH status ด้วย status ที่ไม่ถูกต้อง

## Phase 8: Verify

- [x] รัน `pytest --cov=app --cov-report=term-missing` ผ่านทั้งหมด
- [x] รัน server และทดสอบผ่าน Swagger UI ที่ `/docs`
- [x] อัปเดต README ให้ตรงกับ implementation จริง
