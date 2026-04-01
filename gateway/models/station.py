from pydantic import BaseModel, Field, ConfigDict

class StationBase(BaseModel):
    name: str = Field(..., description="Name of the fuel station", example="Central Super Point")
    location: str = Field(..., description="City or area of the station", example="Colombo 07")

class StationResponse(StationBase):
    id: str = Field(alias="_id", description="Unique identifier of the station")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
