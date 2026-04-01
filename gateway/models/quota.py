from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class QuotaBase(BaseModel):
    vehicleId: str = Field(..., description="Vehicle ID", example="65e1234567890abcdef12345")
    weekStartDate: str = Field(..., description="The start date of the week for this quota (YYYY-MM-DD, usually a Sunday)", example="2026-03-29")
    allocatedLiters: float = Field(..., description="Total liters", example=20.0)
    consumedLiters: float = Field(..., description="Consumed liters", example=5.5)

class QuotaCreate(QuotaBase):
    pass

class QuotaUpdate(BaseModel):
    vehicleId: Optional[str] = Field(None, description="Updated vehicle ID")
    weekStartDate: Optional[str] = Field(None, description="Updated week start date (YYYY-MM-DD)")
    allocatedLiters: Optional[float] = Field(None, description="Updated allocated liters")
    consumedLiters: Optional[float] = Field(None, description="Updated consumed liters")

class QuotaResponse(QuotaBase):
    id: str = Field(alias="_id", description="Unique identifier")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
