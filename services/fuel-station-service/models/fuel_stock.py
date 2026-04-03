from datetime import date
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic import field_validator


class FuelStockCreate(BaseModel):
    stationId: str = Field(..., example="650c1f2e1c4e4a0012345678")
    fuelType: str = Field(..., min_length=1, example="Petrol 92")
    date: date = Field(..., example="2026-04-03", description="Daily stock date (YYYY-MM-DD)")

    dailyQuota: float = Field(..., gt=0, example=5000.0, description="Total available quota for the day (liters)")
    receivedLiters: float = Field(..., ge=0, example=1500.0, description="Liters received into stock for the day")
    availableLiters: Optional[float] = Field(
        None,
        ge=0,
        example=1500.0,
        description="Liters available to serve (defaults to receivedLiters on creation)",
    )
    transactions: List[str] = Field(default_factory=list, description="Transaction IDs associated with this daily stock")

    @field_validator("fuelType")
    @classmethod
    def normalize_fuel_type(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("fuelType must be non-empty")
        return v

    model_config = ConfigDict(populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True)


class FuelStockUpdate(BaseModel):
    stationId: Optional[str] = Field(None, example="650c1f2e1c4e4a0012345678")
    fuelType: Optional[str] = Field(None, min_length=1, example="Petrol 92")
    date: Optional[date] = Field(None, example="2026-04-03")

    dailyQuota: Optional[float] = Field(None, gt=0, example=5000.0)
    receivedLiters: Optional[float] = Field(None, ge=0, example=2000.0)
    availableLiters: Optional[float] = Field(None, ge=0, example=1750.0)
    transactions: Optional[List[str]] = Field(None, description="Replace transactions list for this record")

    @field_validator("fuelType")
    @classmethod
    def normalize_update_fuel_type(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            raise ValueError("fuelType must be non-empty")
        return v

    model_config = ConfigDict(populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True)


class FuelStockResponse(BaseModel):
    id: str = Field(alias="_id")
    stationId: str
    fuelType: str
    date: date

    dailyQuota: float
    availableLiters: float
    receivedLiters: float
    transactions: List[str]

    model_config = ConfigDict(populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True)


class FuelStockDeduct(BaseModel):
    stationId: str = Field(..., example="650c1f2e1c4e4a0012345678")
    fuelType: str = Field(..., min_length=1, example="Petrol 92")
    liters: float = Field(..., gt=0, example=10.5, description="Liters to deduct from availableLiters")
    date: Optional[date] = Field(None, example="2026-04-03", description="Optional stock date (defaults to today)")
    transactionId: Optional[str] = Field(None, example="650c1f2e1c4e4a0099999999")

    @field_validator("fuelType")
    @classmethod
    def normalize_deduct_fuel_type(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("fuelType must be non-empty")
        return v

    model_config = ConfigDict(populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True)

