from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from utils.mongo_helper import PyObjectId

class CitizenBase(BaseModel):
    name: str = Field(..., description="Full name of the citizen", example="John Doe")
    NIC: str = Field(..., description="National Identity Card number", example="123456789V")

class CitizenCreate(CitizenBase):
    pass

class CitizenUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated name of the citizen", example="John A. Doe")
    NIC: Optional[str] = Field(None, description="Updated NIC number", example="123456789V")
    registeredVehicles: Optional[List[str]] = Field(None, description="Updated list of vehicle IDs registered to the citizen")

class CitizenResponse(CitizenBase):
    id: str = Field(alias="_id", description="Unique identifier of the citizen (MongoDB ObjectId as string)")
    registeredVehicles: List[str] = Field(default=[], description="List of vehicle IDs registered to this citizen")
    registeredAt: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of registration")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
