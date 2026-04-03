from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer
from services.citizen_vehicle_services import CitizenService
from models.citizen import CitizenResponse, CitizenCreate, CitizenUpdate
from utils.auth import role_required
from typing import List

router = APIRouter()
service = CitizenService()
security = HTTPBearer()

@router.get("/", 
            response_model=List[CitizenResponse],
            summary="List all citizens",
            tags=["Citizens"],
            dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def get_citizens(request: Request):
    return await service.get_all(request)

@router.get("/{citizen_id}", 
            response_model=CitizenResponse,
            summary="Get citizen by ID",
            tags=["Citizens"],
            dependencies=[Depends(role_required(["admin", "station_operator", "citizen"])), Depends(security)])
async def get_citizen(citizen_id: str, request: Request):
    return await service.get_by_id(citizen_id, request)

@router.post("/", 
             response_model=CitizenResponse, 
             summary="Create a new citizen",
             tags=["Citizens"])
async def create_citizen(citizen: CitizenCreate, request: Request):
    return await service.create(citizen.model_dump(), request)

@router.put("/{citizen_id}",
            response_model=CitizenResponse,
            summary="Update citizen details",
            tags=["Citizens"],
            dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def update_citizen(citizen_id: str, citizen: CitizenUpdate, request: Request):
    return await service.update(citizen_id, citizen.model_dump(), request)

@router.delete("/{citizen_id}",
               summary="Delete a citizen",
               tags=["Citizens"],
               dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def delete_citizen(citizen_id: str, request: Request):
    return await service.delete(citizen_id, request)
