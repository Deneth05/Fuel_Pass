from pydantic import BaseModel, Field, ConfigDict

from typing import List, Optional

class StationBase(BaseModel):
    name: str = Field(..., description="Name of the fuel station", example="Central Super Point")
    location: str = Field(..., description="City or area of the station", example="Colombo 07")
    fuelTypes: List[str] = Field(..., example=["Petrol 92", "Diesel"], description="List of supported fuel types")

class StationCreate(StationBase):
    pass

class StationUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Station Name")
    location: Optional[str] = Field(None, example="Updated location")
    fuelTypes: Optional[List[str]] = Field(None, example=["Petrol 95", "Diesel"])

class StationResponse(StationBase):
    id: str = Field(alias="_id", description="Unique identifier of the station")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
