from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum
from utils.mongo_helper import PyObjectId

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
    citizenId: str = Field(..., description="ID of the citizen who owns the vehicle", example="65e1234567890abcdef12345")
    vehicleNumber: str = Field(..., description="Unique license plate number", example="ABC-1234")
    fuelType: FuelType = Field(..., description="Type of fuel the vehicle uses", example="Petrol")
    vehicleType: VehicleType = Field(..., description="Type of the vehicle", example="Car")

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    citizenId: Optional[str] = Field(None, description="Updated citizen ID")
    vehicleNumber: Optional[str] = Field(None, description="Updated vehicle number")
    fuelType: Optional[FuelType] = Field(None, description="Updated fuel type")
    vehicleType: Optional[VehicleType] = Field(None, description="Updated vehicle type")

class VehicleResponse(VehicleBase):
    id: str = Field(alias="_id", description="Unique identifier of the vehicle")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
