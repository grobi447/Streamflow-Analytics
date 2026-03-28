from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth
from app.database.repositories.user_repository import UserRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    UserRepository().init_table()
    yield

app = FastAPI(title="Auth Service", lifespan=lifespan)
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}