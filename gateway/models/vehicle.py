from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class FuelType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"

class VehicleBase(BaseModel):
    citizenId: str = Field(..., description="Owner's citizen ID", example="65e1234567890abcdef12345")
    vehicleNumber: str = Field(..., description="License plate number", example="ABC-1234")
    fuelType: FuelType = Field(..., description="Fuel type", example="Petrol")

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: str = Field(..., description="Unique identifier")
