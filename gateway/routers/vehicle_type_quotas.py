from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from services.citizen_vehicle_services import VehicleTypeQuotaService
from models.vehicle_type_quota import VehicleTypeQuotaResponse, VehicleTypeQuotaCreate
from utils.auth import role_required
from typing import List

router = APIRouter()
service = VehicleTypeQuotaService()
security = HTTPBearer()

@router.post("/", 
             response_model=VehicleTypeQuotaResponse, 
             summary="Create a vehicle type quota",
             tags=["Vehicle Type Quotas"],
             dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def create_vehicle_type_quota(quota: VehicleTypeQuotaCreate, request: Request):
    """
    Create a new vehicle type quota definition.
    """
    return await service.create(quota.model_dump(mode="json"), request)

@router.get("/", 
            response_model=List[VehicleTypeQuotaResponse],
            summary="List all vehicle type quotas",
            tags=["Vehicle Type Quotas"],
            dependencies=[Depends(role_required(["admin", "manager"])), Depends(security)])
async def list_vehicle_type_quotas(request: Request):
    """
    Retrieve all vehicle type quota records via the gateway.
    """
    return await service.get_all(request)

@router.get("/{vehicle_type}", 
            response_model=VehicleTypeQuotaResponse,
            summary="Get quota for a specific vehicle type",
            tags=["Vehicle Type Quotas"],
            dependencies=[Depends(role_required(["admin", "manager"])), Depends(security)])
async def get_vehicle_type_quota(vehicle_type: str, request: Request):
    """
    Retrieve quota details for a specific vehicle type via the gateway.
    """
    return await service.get_by_type(vehicle_type, request)

@router.put("/{vehicle_type}", 
            response_model=VehicleTypeQuotaResponse,
            summary="Update an existing vehicle type quota",
            tags=["Vehicle Type Quotas"],
            dependencies=[Depends(role_required(["admin", "manager"])), Depends(security)])
async def update_vehicle_type_quota(vehicle_type: str, data: dict, request: Request):
    """
    Update the fuel liters per week for a specific vehicle type via the gateway.
    """
    return await service.update(vehicle_type, data, request)

@router.delete("/{vehicle_type}", 
               summary="Delete a vehicle type quota",
               tags=["Vehicle Type Quotas"],
               dependencies=[Depends(role_required(["admin", "manager"])), Depends(security)])
async def delete_vehicle_type_quota(vehicle_type: str, request: Request):
    """
    Remove the quota definition for a specific vehicle type via the gateway.
    """
    return await service.delete(vehicle_type, request)
