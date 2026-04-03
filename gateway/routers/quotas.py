from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer
from services.citizen_vehicle_services import QuotaService
from models.quota import QuotaResponse, QuotaUpdate, QuotaCreate
from utils.auth import role_required
from typing import List

router = APIRouter()
service = QuotaService()
security = HTTPBearer()

@router.get("/", 
            response_model=List[QuotaResponse],
            summary="List all quotas",
            tags=["Quotas"],
            dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def get_quotas(request: Request):
    return await service.get_all(request)

@router.get("/{id}", 
            response_model=QuotaResponse,
            summary="Get quota by ID",
            tags=["Quotas"],
            dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def get_quota(id: str, request: Request):
    return await service.get_by_id(id, request)

@router.get("/citizen/{citizen_id}", 
            response_model=List[QuotaResponse],
            summary="List quotas by citizen",
            tags=["Quotas"],
            dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def get_by_citizen(citizen_id: str, request: Request):
    return await service.get_by_citizen(citizen_id, request)

@router.post("/", 
             response_model=QuotaResponse, 
             summary="Manually create a quota",
             tags=["Quotas"],
             dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def create_quota(quota: QuotaCreate, request: Request):
    return await service.create(quota.model_dump(mode="json"), request)

@router.put("/renew-all", 
            summary="Renew all quotas for the new month",
            tags=["Quotas"],
            dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def renew_all(request: Request):
    return await service.renew_all(request)

@router.put("/{id}", 
            response_model=QuotaResponse,
            summary="Update quota details",
            tags=["Quotas"],
            dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def update_quota(id: str, quota: QuotaUpdate, request: Request):
    return await service.update(id, quota.model_dump(mode="json"), request)

@router.delete("/{id}", 
               summary="Delete a quota",
               tags=["Quotas"],
               dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def delete_quota(id: str, request: Request):
    return await service.delete(id, request)
