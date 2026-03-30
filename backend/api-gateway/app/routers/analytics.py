import httpx
from fastapi import APIRouter, Depends
from app.config import settings
from app.middleware.auth_middleware import verify_token

router = APIRouter()

@router.get("/analytics/summary")
async def get_summary(user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ANALYTICS_SERVICE_URL}/analytics/summary")
        return response.json()

@router.get("/analytics/device/{device_id}")
async def get_device(device_id: str, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ANALYTICS_SERVICE_URL}/analytics/device/{device_id}")
        return response.json()

@router.get("/analytics/location/{location}")
async def get_location(location: str, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ANALYTICS_SERVICE_URL}/analytics/location/{location}")
        return response.json()

@router.get("/analytics/top-latency")
async def get_top_latency(limit: int = 10, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ANALYTICS_SERVICE_URL}/analytics/top-latency?limit={limit}")
        return response.json()

@router.get("/analytics/trends")
async def get_trends(hours: int = 24, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ANALYTICS_SERVICE_URL}/analytics/trends?hours={hours}")
        return response.json()

@router.get("/analytics/devices")
async def get_all_devices(user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ANALYTICS_SERVICE_URL}/analytics/devices")
        return response.json()
    
@router.get("/analytics/trends")
async def get_trends(minutes: int = 60, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.ANALYTICS_SERVICE_URL}/analytics/trends?minutes={minutes}"
        )
        return response.json()
    
@router.get("/analytics/latest-devices")
async def get_latest_devices(user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ANALYTICS_SERVICE_URL}/analytics/latest-devices")
        return response.json()