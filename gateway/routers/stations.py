from fastapi import APIRouter, status, Request, Depends
from fastapi.security import HTTPBearer
from services.station_stock_services import StationService
from models.station import StationResponse, StationCreate, StationUpdate
from utils.auth import role_required
from typing import List

router = APIRouter()
service = StationService()
security = HTTPBearer()

@router.post("/register", 
             response_model=StationResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Register a new station (Open)",
             tags=["Stations"]) # Public registration
async def register_station(station: StationCreate, request: Request):
    return await service.create(station.model_dump(mode="json"), request)

@router.post("/", 
             response_model=StationResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new station (Admin only)",
             tags=["Stations"],
             dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def create_station(station: StationCreate, request: Request):
    return await service.create(station.model_dump(mode="json"), request)

@router.get("/", 
            response_model=List[StationResponse],
            summary="List all fuel stations",
            tags=["Stations"],
            dependencies=[Depends(security)]) # Secured but all roles
async def get_stations(request: Request):
    return await service.get_all(request)

@router.get("/{station_id}", 
            response_model=StationResponse,
            summary="Get station by ID",
            tags=["Stations"],
            dependencies=[Depends(security)]) # Secured but all roles
async def get_station(station_id: str, request: Request):
    return await service.get_by_id(station_id, request)

@router.put("/{station_id}", 
            response_model=StationResponse,
            summary="Update station details",
            tags=["Stations"],
            dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def update_station(station_id: str, station_update: StationUpdate, request: Request):
    return await service.update(station_id, station_update.model_dump(mode="json", exclude_none=True), request)

@router.delete("/{station_id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a station",
               tags=["Stations"],
               dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def delete_station(station_id: str, request: Request):
    return await service.delete(station_id, request)
