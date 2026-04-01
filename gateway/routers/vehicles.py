from fastapi import APIRouter
from services.citizen_vehicle_services import VehicleService
from models.vehicle import VehicleResponse, VehicleCreate, VehicleUpdate
from typing import List

router = APIRouter()
service = VehicleService()

@router.get("/", 
            response_model=List[VehicleResponse],
            summary="List all vehicles",
            tags=["Vehicles"])
async def get_vehicles():
    """
    Retrieve all registered vehicles via the gateway.
    """
    return await service.get_all()

@router.get("/{vehicle_id}", 
            response_model=VehicleResponse,
            summary="Get vehicle by ID",
            tags=["Vehicles"])
async def get_vehicle(vehicle_id: str):
    """
    Retrieve a specific vehicle's details via the gateway.
    """
    return await service.get_by_id(vehicle_id)

@router.post("/", 
             response_model=VehicleResponse,
             summary="Register a new vehicle",
             tags=["Vehicles"])
async def create_vehicle(vehicle: VehicleCreate):
    """
    Register a vehicle for a citizen via the gateway.
    """
    return await service.create(vehicle.model_dump())

@router.put("/{vehicle_id}",
            response_model=VehicleResponse,
            summary="Update vehicle details",
            tags=["Vehicles"])
async def update_vehicle(vehicle_id: str, vehicle: VehicleUpdate):
    """
    Update vehicle information via the gateway.
    """
    return await service.update(vehicle_id, vehicle.model_dump())

@router.delete("/{vehicle_id}",
               summary="Delete a vehicle",
               tags=["Vehicles"])
async def delete_vehicle(vehicle_id: str):
    """
    Remove a vehicle from the system via the gateway.
    """
    return await service.delete(vehicle_id)
