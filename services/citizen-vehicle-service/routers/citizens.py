from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from database.mongo import get_database
from models.citizen import CitizenCreate, CitizenUpdate, CitizenResponse
from datetime import datetime

router = APIRouter()
db = get_database()
collection = db["citizens"]

@router.post("/", 
             response_model=CitizenResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Create a new citizen",
             tags=["Citizens"])
async def create_citizen(citizen: CitizenCreate):
    """
    Register a new citizen in the system.
    Initializes an empty list of registered vehicles.
    """
    citizen_dict = citizen.model_dump()
    citizen_dict["registeredVehicles"] = []
    citizen_dict["registeredAt"] = datetime.utcnow()
    
    result = await collection.insert_one(citizen_dict)
    created_citizen = await collection.find_one({"_id": result.inserted_id})
    # Convert _id to string for the response model which expects str for 'id' aliased from '_id'
    created_citizen["_id"] = str(created_citizen["_id"])
    return created_citizen

@router.get("/", 
            response_model=List[CitizenResponse],
            summary="List all citizens",
            tags=["Citizens"])
async def list_citizens():
    """
    Retrieve a list of all registered citizens.
    Returns up to 100 records.
    """
    citizens = await collection.find().to_list(100)
    for c in citizens:
        c["_id"] = str(c["_id"])
    return citizens

@router.get("/{id}", 
            response_model=CitizenResponse,
            summary="Get citizen by ID",
            tags=["Citizens"])
async def get_citizen(id: str):
    """
    Retrieve details of a specific citizen by their unique database ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    citizen = await collection.find_one({"_id": ObjectId(id)})
    if citizen is None:
        raise HTTPException(status_code=404, detail=f"Citizen with id {id} not found")
    
    citizen["_id"] = str(citizen["_id"])
    return citizen

@router.put("/{id}", 
            response_model=CitizenResponse,
            summary="Update citizen details",
            tags=["Citizens"])
async def update_citizen(id: str, citizen_update: CitizenUpdate):
    """
    Update information for an existing citizen.
    Only provided fields will be updated.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in citizen_update.model_dump().items() if v is not None}
    
    if len(update_data) >= 1:
        update_result = await collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Citizen with id {id} not found")

    updated_citizen = await collection.find_one({"_id": ObjectId(id)})
    if updated_citizen is None:
        raise HTTPException(status_code=404, detail=f"Citizen with id {id} not found")
    
    updated_citizen["_id"] = str(updated_citizen["_id"])
    return updated_citizen

@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a citizen",
               tags=["Citizens"])
async def delete_citizen(id: str):
    """
    Remove a citizen from the system by their ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Citizen with id {id} not found")
    return None
