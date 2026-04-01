from pydantic import BaseModel, Field

class StationBase(BaseModel):
    name: str = Field(..., description="Name of the fuel station", example="Central Super Point")
    location: str = Field(..., description="City or area of the station", example="Colombo 07")

class StationResponse(StationBase):
    id: str = Field(..., description="Unique identifier of the station")
