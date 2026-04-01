from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class QueueStatus(str, Enum):
    WAITING = "waiting"
    SERVED = "served"
    CANCELLED = "cancelled"

class QueueJoin(BaseModel):
    stationId: str = Field(..., description="ID of the fuel station", example="STN001")
    vehicleId: str = Field(..., description="ID of the vehicle", example="VHL123")
    requestedLiters: float = Field(..., gt=0, description="Amount of fuel requested in liters", example=20.0)

class QueueUpdate(BaseModel):
    status: Optional[QueueStatus] = None
    requestedLiters: Optional[float] = Field(None, gt=0)

class QueueResponse(BaseModel):
    id: str = Field(..., description="Queue entry ID")
    stationId: str = Field(..., description="Station ID")
    vehicleId: str = Field(..., description="Vehicle ID")
    requestedLiters: float = Field(..., description="Requested liters")
    status: QueueStatus = Field(..., description="Queue status")
    joinedAt: datetime = Field(..., description="Time joined")
