from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class StationBase(BaseModel):
    registrationNumber: Optional[str] = Field(None, min_length=1, max_length=50, example="REG123456", description="Unique registration number of the station")
    name: str = Field(..., min_length=1, max_length=100, description="Name of the fuel station", example="Central Super Point")
    location: str = Field(..., min_length=1, max_length=250, description="City or area of the station", example="Colombo 07")
    fuelTypes: List[str] = Field(..., min_length=1, example=["Petrol 92", "Diesel"], description="List of supported fuel types")

class StationCreate(StationBase):
    registrationNumber: str = Field(..., min_length=1, max_length=50, example="REG123456")

class StationUpdate(BaseModel):
    registrationNumber: Optional[str] = Field(None, min_length=1, max_length=50, example="REG654321")
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Updated Station Name")
    location: Optional[str] = Field(None, min_length=1, max_length=250, example="Updated location")
    fuelTypes: Optional[List[str]] = Field(None, min_length=1, example=["Petrol 95", "Diesel"])

class StationResponse(StationBase):
    id: str = Field(alias="_id", description="Unique identifier of the station")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
