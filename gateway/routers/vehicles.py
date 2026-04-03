from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer
from services.citizen_vehicle_services import VehicleService
from models.vehicle import VehicleResponse, VehicleCreate, VehicleUpdate
from utils.auth import role_required
from typing import List

router = APIRouter()
service = VehicleService()
security = HTTPBearer()

@router.get("/", 
            response_model=List[VehicleResponse],
            summary="List all vehicles",
            tags=["Vehicles"],
            dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def get_vehicles(request: Request):
    return await service.get_all(request)

@router.get("/{vehicle_id}", 
            response_model=VehicleResponse,
            summary="Get vehicle by ID",
            tags=["Vehicles"],
            dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def get_vehicle(vehicle_id: str, request: Request):
    return await service.get_by_id(vehicle_id, request)

@router.post("/", 
             response_model=VehicleResponse,
             summary="Register a new vehicle",
             tags=["Vehicles"],
             dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def create_vehicle(vehicle: VehicleCreate, request: Request):
    return await service.create(vehicle.model_dump(mode="json"), request)

@router.put("/{vehicle_id}",
            response_model=VehicleResponse,
            summary="Update vehicle details",
            tags=["Vehicles"],
            dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate, request: Request):
    return await service.update(vehicle_id, vehicle.model_dump(mode="json"), request)

@router.delete("/{vehicle_id}",
               summary="Delete a vehicle",
               tags=["Vehicles"],
               dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def delete_vehicle(vehicle_id: str, request: Request):
    return await service.delete(vehicle_id, request)
