from pydantic import BaseModel, Field
from typing import Optional

class QuotaBase(BaseModel):
    vehicleId: str = Field(..., description="Vehicle ID", example="65e1234567890abcdef12345")
    month: str = Field(..., description="Month (YYYY-MM)", example="2026-03")
    allocatedLiters: float = Field(..., description="Total liters", example=20.0)
    consumedLiters: float = Field(..., description="Consumed liters", example=5.5)

class QuotaResponse(QuotaBase):
    id: str = Field(..., description="Unique identifier")
