from fastapi import APIRouter
from services.citizen_vehicle_services import CitizenService
from models.citizen import CitizenResponse, CitizenCreate, CitizenUpdate
from typing import List

router = APIRouter()
service = CitizenService()

@router.get("/", 
            response_model=List[CitizenResponse],
            summary="List all citizens",
            tags=["Citizens"])
async def get_citizens():
    """
    Retrieve all citizens through the gateway.
    """
    return await service.get_all()

@router.get("/{citizen_id}", 
            response_model=CitizenResponse,
            summary="Get citizen by ID",
            tags=["Citizens"])
async def get_citizen(citizen_id: str):
    """
    Retrieve a specific citizen's details via the gateway.
    """
    return await service.get_by_id(citizen_id)

@router.post("/", 
             response_model=CitizenResponse,
             summary="Create a new citizen",
             tags=["Citizens"])
async def create_citizen(citizen: CitizenCreate):
    """
    Register a new citizen via the gateway.
    """
    return await service.create(citizen.model_dump())

@router.put("/{citizen_id}",
            response_model=CitizenResponse,
            summary="Update citizen details",
            tags=["Citizens"])
async def update_citizen(citizen_id: str, citizen: CitizenUpdate):
    """
    Update an existing citizen's details via the gateway.
    """
    return await service.update(citizen_id, citizen.model_dump())

@router.delete("/{citizen_id}",
               summary="Delete a citizen",
               tags=["Citizens"])
async def delete_citizen(citizen_id: str):
    """
    Delete a citizen's record via the gateway.
    """
    return await service.delete(citizen_id)
