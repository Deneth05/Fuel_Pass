from pydantic import BaseModel, Field, ConfigDict

class FuelStockBase(BaseModel):
    stationId: str = Field(..., description="Station ID", example="STN001")
    fuelType: str = Field(..., description="Type of fuel", example="Petrol")
    availableLiters: float = Field(..., description="Current stock in liters", example=5000.0)

class FuelStockResponse(FuelStockBase):
    id: str = Field(alias="_id", description="Unique identifier of the stock record")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
