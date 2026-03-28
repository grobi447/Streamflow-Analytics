from pydantic import BaseModel
from datetime import datetime

class IngestResponse(BaseModel):
    status: str
    event_id: str
    device_id: str
    timestamp: datetime
    message: str

class ErrorResponse(BaseModel):
    status: str
    message: str
    detail: str