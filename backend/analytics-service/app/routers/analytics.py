from fastapi import APIRouter, HTTPException
from typing import List
from app.models.analytics import (
    DeviceSummary,
    LocationSummary,
    TrendPoint,
    TopLatencyDevice,
    NetworkSummary
)
from app.services.analytics_service import analytics_service

router = APIRouter()

@router.get("/summary", response_model=NetworkSummary)
async def get_summary() -> NetworkSummary:
    try:
        return analytics_service.get_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/device/{device_id}", response_model=DeviceSummary)
async def get_device(device_id: str) -> DeviceSummary:
    try:
        return analytics_service.get_device(device_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/location/{location}", response_model=LocationSummary)
async def get_location(location: str) -> LocationSummary:
    try:
        return analytics_service.get_location(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-latency", response_model=List[TopLatencyDevice])
async def get_top_latency(limit: int = 10) -> List[TopLatencyDevice]:
    try:
        return analytics_service.get_top_latency(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends", response_model=List[TrendPoint])
async def get_trends(hours: int = 24) -> List[TrendPoint]:
    try:
        return analytics_service.get_trends(hours)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))