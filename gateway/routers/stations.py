from fastapi import APIRouter, status
from services.station_stock_services import StationService
from models.station import StationResponse, StationCreate, StationUpdate
from typing import List

router = APIRouter()
service = StationService()

@router.post("/", 
             response_model=StationResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new station",
             tags=["Stations"])
async def create_station(station: StationCreate):
    """
    Create a new fuel station via the gateway.
    """
    return await service.create(station.model_dump())

@router.get("/", 
            response_model=List[StationResponse],
            summary="List all fuel stations",
            tags=["Stations"])
async def get_stations():
    """
    Retrieve all fuel stations via the gateway.
    """
    return await service.get_all()

@router.get("/{station_id}", 
            response_model=StationResponse,
            summary="Get station by ID",
            tags=["Stations"])
async def get_station(station_id: str):
    """
    Retrieve details of a specific fuel station.
    """
    return await service.get_by_id(station_id)

@router.put("/{station_id}", 
            response_model=StationResponse,
            summary="Update station details",
            tags=["Stations"])
async def update_station(station_id: str, station_update: StationUpdate):
    """
    Update a fuel station's information.
    """
    return await service.update(station_id, station_update.model_dump(exclude_none=True))

@router.delete("/{station_id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a station",
               tags=["Stations"])
async def delete_station(station_id: str):
    """
    Remove a fuel station from the system.
    """
    return await service.delete(station_id)
