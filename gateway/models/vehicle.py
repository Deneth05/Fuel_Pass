from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class FuelType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"

class VehicleType(str, Enum):
    BUS = "Bus"
    LORRY = "Lorry"
    VAN = "Van"
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"
    THREE_WHEELER = "Three Wheeler"
    CAB = "Cab"

class VehicleBase(BaseModel):
    citizenId: str = Field(..., description="Owner's citizen ID", example="65e1234567890abcdef12345")
    vehicleNumber: str = Field(..., description="License plate number", example="ABC-1234")
    fuelType: FuelType = Field(..., description="Fuel type", example="Petrol")
    vehicleType: VehicleType = Field(..., description="Type of the vehicle", example="Car")

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    citizenId: Optional[str] = Field(None, description="Updated citizen ID")
    vehicleNumber: Optional[str] = Field(None, description="Updated vehicle number")
    fuelType: Optional[FuelType] = Field(None, description="Updated fuel type")
    vehicleType: Optional[VehicleType] = Field(None, description="Updated vehicle type")

class VehicleResponse(VehicleBase):
    id: str = Field(alias="_id", description="Unique identifier")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
