from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class TransactionBase(BaseModel):
    vehicleId: str = Field(..., example="650c1f2e1c4e4a0012345678")
    stationId: str = Field(..., example="650c1f2e1c4e4a0012345679")
    fuelType: str = Field(..., example="Petrol 92")
    litersServed: float = Field(..., gt=0, example=10.5)

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    vehicleId: Optional[str] = Field(None, example="650c1f2e1c4e4a0012345678")
    stationId: Optional[str] = Field(None, example="650c1f2e1c4e4a0012345679")
    fuelType: Optional[str] = Field(None, example="Petrol 92")
    litersServed: Optional[float] = Field(None, gt=0, example=10.5)

class Transaction(TransactionBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    transactionTime: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "vehicleId": "650c1f2e1c4e4a0012345678",
                "stationId": "650c1f2e1c4e4a0012345679",
                "fuelType": "Petrol 92",
                "litersServed": 10.5,
                "transactionTime": "2023-10-27T10:00:00Z"
            }
        }

class TransactionResponse(Transaction):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
