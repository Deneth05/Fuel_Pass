from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TransactionBase(BaseModel):
    vehicleId: str = Field(..., description="Vehicle ID", example="VEH789")
    stationId: str = Field(..., description="Station ID", example="STN001")
    liters: float = Field(..., description="Amount of fuel pumped", example=15.5)

class TransactionResponse(TransactionBase):
    id: str = Field(alias="_id", description="Unique identifier")
    timestamp: datetime = Field(..., description="Time of transaction")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
