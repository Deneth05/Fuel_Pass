from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CitizenBase(BaseModel):
    name: str = Field(..., description="Full name of the citizen", example="John Doe")
    NIC: str = Field(..., description="National Identity Card number", example="123456789V")

class CitizenCreate(CitizenBase):
    pass

class CitizenResponse(CitizenBase):
    id: str = Field(..., description="Unique identifier")
    registeredVehicles: List[str] = Field(default=[], description="List of vehicle IDs")
    registeredAt: datetime = Field(..., description="Registration timestamp")
