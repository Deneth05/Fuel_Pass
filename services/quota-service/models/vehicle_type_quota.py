from pydantic import BaseModel, Field, ConfigDict
from models.vehicle_types import VehicleType
from typing import Optional
from utils.mongo_helper import PyObjectId

class VehicleTypeQuotaBase(BaseModel):
    vehicleType: VehicleType = Field(..., description="Vehicle type this quota applies to", example="Car")
    litersPerWeek: float = Field(..., description="Fuel liters allocated per week", example=20.0)

class VehicleTypeQuotaCreate(VehicleTypeQuotaBase):
    pass

class VehicleTypeQuotaUpdate(BaseModel):
    litersPerWeek: Optional[float] = Field(None, description="Update liters per week")

class VehicleTypeQuotaResponse(VehicleTypeQuotaBase):
    id: str = Field(alias="_id", description="Unique identifier")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
