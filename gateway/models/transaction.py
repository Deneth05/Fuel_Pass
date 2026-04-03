from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TransactionBase(BaseModel):
    vehicleId: str = Field(..., description="Vehicle ID", example="650c1f2e1c4e4a0012345678")
    stationId: str = Field(..., description="Station ID", example="650c1f2e1c4e4a0012345679")
    fuelType: str = Field(..., description="Type of fuel", example="Petrol 92")
    litersServed: float = Field(..., description="Amount of fuel pumped", example=15.5)

class TransactionResponse(TransactionBase):
    id: str = Field(alias="_id", description="Unique identifier")
    transactionTime: datetime = Field(..., description="Time of transaction")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
