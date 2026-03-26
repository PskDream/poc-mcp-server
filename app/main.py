from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Todo Management API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)
