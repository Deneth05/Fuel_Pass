from pydantic import BaseModel, Field
from datetime import datetime

class TransactionBase(BaseModel):
    vehicleId: str = Field(..., description="Vehicle ID", example="VEH789")
    stationId: str = Field(..., description="Station ID", example="STN001")
    liters: float = Field(..., description="Amount of fuel pumped", example=15.5)

class TransactionResponse(TransactionBase):
    id: str = Field(..., description="Unique identifier")
    timestamp: datetime = Field(..., description="Time of transaction")
