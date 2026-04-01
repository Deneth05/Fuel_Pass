from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from utils.mongo_helper import PyObjectId

class QuotaBase(BaseModel):
    vehicleId: str = Field(..., description="ID of the vehicle the quota belongs to", example="65e1234567890abcdef12345")
    month: str = Field(..., description="The month for which the quota is allocated (YYYY-MM)", example="2026-03")
    allocatedLiters: float = Field(..., description="Total fuel liters allocated for the month", example=20.0)
    consumedLiters: float = Field(default=0.0, description="Amount of fuel already consumed from the quota", example=5.5)

class QuotaCreate(QuotaBase):
    pass

class QuotaUpdate(BaseModel):
    vehicleId: Optional[str] = Field(None, description="Updated vehicle ID")
    month: Optional[str] = Field(None, description="Updated month (YYYY-MM)")
    allocatedLiters: Optional[float] = Field(None, description="Updated allocated liters")
    consumedLiters: Optional[float] = Field(None, description="Updated consumed liters")

class QuotaResponse(QuotaBase):
    id: str = Field(alias="_id", description="Unique identifier of the quota record")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
