from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class QueueStatus(str, Enum):
    WAITING = "waiting"
    SERVED = "served"
    CANCELLED = "cancelled"

class QueueBase(BaseModel):
    stationId: str = Field(..., description="ID of the fuel station")
    vehicleId: str = Field(..., description="ID of the vehicle")
    requestedLiters: float = Field(..., gt=0, description="Amount of fuel requested in liters")

class QueueCreate(QueueBase):
    pass

class QueueUpdate(BaseModel):
    status: Optional[QueueStatus] = None
    requestedLiters: Optional[float] = Field(None, gt=0)

class QueueResponse(QueueBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    id: str = Field(alias="_id")
    status: QueueStatus
    joinedAt: datetime
