from pydantic import BaseModel, Field

class QueueJoin(BaseModel):
    citizenId: str = Field(..., description="ID of the citizen joining the queue", example="65e1234567890abcdef12345")
    stationId: str = Field(..., description="ID of the fuel station", example="STN001")
    vehicleType: str = Field(..., description="Type of vehicle", example="Car")

class QueueResponse(BaseModel):
    id: str = Field(..., description="Queue entry ID")
    position: int = Field(..., description="Current position in queue", example=5)
    status: str = Field(..., description="Queue status", example="Waiting")
