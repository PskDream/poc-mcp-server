from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import tasks
from app.mcp_server import mcp


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    async with mcp.session_manager.run():
        yield


app = FastAPI(
    title="Todo Management API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)
app.mount("/mcp", mcp.streamable_http_app())
