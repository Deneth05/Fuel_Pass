from pydantic import BaseModel, Field, ConfigDict

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import date as dt_date

class FuelStockBase(BaseModel):
    stationId: str = Field(..., description="Station ID", example="650c1f2e1c4e4a0012345678")
    fuelType: str = Field(..., description="Type of fuel", example="Petrol 92")
    date: dt_date = Field(..., description="Daily stock date (YYYY-MM-DD)", example="2026-04-03")

class FuelStockCreate(FuelStockBase):
    dailyQuota: float = Field(..., gt=0, example=5000.0)
    receivedLiters: float = Field(..., ge=0, example=1500.0)
    availableLiters: Optional[float] = Field(None, ge=0, example=1500.0)

class FuelStockUpdate(BaseModel):
    stationId: Optional[str] = Field(None, example="650c1f2e1c4e4a0012345678")
    fuelType: Optional[str] = Field(None, example="Petrol 92")
    date: Optional[dt_date] = Field(None, example="2026-04-03")
    dailyQuota: Optional[float] = Field(None, gt=0, example=5000.0)
    receivedLiters: Optional[float] = Field(None, ge=0, example=2000.0)
    availableLiters: Optional[float] = Field(None, ge=0, example=1750.0)
    transactions: Optional[List[str]] = Field(None)

class FuelStockResponse(FuelStockBase):
    id: str = Field(alias="_id", description="Unique identifier of the stock record")
    dailyQuota: float
    availableLiters: float
    receivedLiters: float
    transactions: List[str]

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class FuelStockDeduct(BaseModel):
    stationId: str = Field(..., example="650c1f2e1c4e4a0012345678")
    fuelType: str = Field(..., example="Petrol 92")
    liters: float = Field(..., gt=0, example=10.5)
    date: Optional[dt_date] = Field(None, example="2026-04-03")
    transactionId: Optional[str] = Field(None, example="650c1f2e1c4e4a0099999999")
