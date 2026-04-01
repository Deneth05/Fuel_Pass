from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class CitizenBase(BaseModel):
    name: str = Field(..., description="Full name of the citizen", example="John Doe")
    NIC: str = Field(..., description="National Identity Card number", example="123456789V")
    email: str = Field(..., description="Email address of the citizen", example="john@example.com")
    mobileNumber: str = Field(..., description="Mobile number of the citizen", example="0771234567")

class CitizenCreate(CitizenBase):
    password: str = Field(..., description="Password for account registration", example="securepassword123")

class CitizenUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated name of the citizen", example="John A. Doe")
    NIC: Optional[str] = Field(None, description="Updated NIC number", example="123456789V")
    email: Optional[str] = Field(None, description="Updated email address", example="john.new@example.com")
    mobileNumber: Optional[str] = Field(None, description="Updated mobile number", example="0779876543")
    registeredVehicles: Optional[List[str]] = Field(None, description="Updated list of vehicle IDs registered to the citizen")

class CitizenResponse(CitizenBase):
    id: str = Field(alias="_id", description="Unique identifier")
    registeredVehicles: List[str] = Field(default=[], description="List of vehicle IDs")
    registeredAt: datetime = Field(..., description="Registration timestamp")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
