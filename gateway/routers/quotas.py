from fastapi import APIRouter
from services.citizen_vehicle_services import QuotaService
from models.quota import QuotaResponse, QuotaUpdate, QuotaCreate
from typing import List

router = APIRouter()
service = QuotaService()

@router.get("/", 
            response_model=List[QuotaResponse],
            summary="List all quotas",
            tags=["Quotas"])
async def get_quotas():
    """
    Retrieve all fuel quota records via the gateway.
    """
    return await service.get_all()

@router.get("/{quota_id}", 
            response_model=QuotaResponse,
            summary="Get quota by ID",
            tags=["Quotas"])
async def get_quota(quota_id: str):
    """
    Retrieve a specific quota record by its ID via the gateway.
    """
    return await service.get_by_id(quota_id)

@router.get("/citizen/{citizen_id}", 
            response_model=QuotaResponse,
            summary="Get citizen quota",
            tags=["Quotas"])
async def get_citizen_quota(citizen_id: str):
    """
    Retrieve quota details for a specific citizen's vehicle via the gateway.
    """
    return await service.get_by_citizen(citizen_id)

@router.post("/", 
             response_model=QuotaResponse,
             summary="Create a fuel quota",
             tags=["Quotas"])
async def create_quota(quota: QuotaCreate):
    """
    Allocate a new fuel quota via the gateway.
    """
    return await service.create(quota.model_dump())

@router.put("/renew-all",
            summary="Renew all vehicle quotas",
            tags=["Quotas"])
async def renew_all_quotas():
    """
    Trigger manual renewal of all quotas via the gateway.
    """
    return await service.renew_all()

@router.put("/{quota_id}",
            response_model=QuotaResponse,
            summary="Update quota details",
            tags=["Quotas"])
async def update_quota(quota_id: str, quota: QuotaUpdate):
    """
    Update an existing fuel quota record via the gateway.
    """
    return await service.update(quota_id, quota.model_dump())

@router.delete("/{quota_id}",
               summary="Delete a quota record",
               tags=["Quotas"])
async def delete_quota(quota_id: str):
    """
    Remove a fuel quota record from the system via the gateway.
    """
    return await service.delete(quota_id)
