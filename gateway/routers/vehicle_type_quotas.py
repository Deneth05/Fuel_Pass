from fastapi import APIRouter
from services.citizen_vehicle_services import VehicleTypeQuotaService
from models.vehicle_type_quota import VehicleTypeQuotaResponse, VehicleTypeQuotaCreate
from typing import List

router = APIRouter()
service = VehicleTypeQuotaService()

@router.post("/", 
             response_model=VehicleTypeQuotaResponse, 
             summary="Create or update a vehicle type quota",
             tags=["Vehicle Type Quotas"])
async def create_vehicle_type_quota(quota: VehicleTypeQuotaCreate):
    """
    Define the fuel liters per week for a specific vehicle type via the gateway.
    """
    return await service.create_or_update(quota.model_dump())

@router.get("/", 
            response_model=List[VehicleTypeQuotaResponse],
            summary="List all vehicle type quotas",
            tags=["Vehicle Type Quotas"])
async def list_vehicle_type_quotas():
    """
    Retrieve all vehicle type quota records via the gateway.
    """
    return await service.get_all()

@router.get("/{vehicle_type}", 
            response_model=VehicleTypeQuotaResponse,
            summary="Get quota for a specific vehicle type",
            tags=["Vehicle Type Quotas"])
async def get_vehicle_type_quota(vehicle_type: str):
    """
    Retrieve quota details for a specific vehicle type via the gateway.
    """
    return await service.get_by_type(vehicle_type)

@router.put("/{vehicle_type}", 
            response_model=VehicleTypeQuotaResponse,
            summary="Update an existing vehicle type quota",
            tags=["Vehicle Type Quotas"])
async def update_vehicle_type_quota(vehicle_type: str, data: dict):
    """
    Update the fuel liters per week for a specific vehicle type via the gateway.
    """
    return await service.update(vehicle_type, data)

@router.delete("/{vehicle_type}", 
               summary="Delete a vehicle type quota",
               tags=["Vehicle Type Quotas"])
async def delete_vehicle_type_quota(vehicle_type: str):
    """
    Remove the quota definition for a specific vehicle type via the gateway.
    """
    return await service.delete(vehicle_type)
