import httpx
from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.post("/auth/login")
async def login(credentials: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.AUTH_SERVICE_URL}/auth/login",
            json=credentials
        )
        return response.json()

@router.post("/auth/register")
async def register(user: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.AUTH_SERVICE_URL}/auth/register",
            json=user
        )
        return response.json()