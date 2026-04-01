from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from database.mongo import get_database
from models.quota import QuotaCreate, QuotaUpdate, QuotaResponse

router = APIRouter()
db = get_database()
collection = db["quotas"]
vehicle_collection = db["vehicles"]

@router.post("/", 
             response_model=QuotaResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Create a fuel quota",
             tags=["Quotas"])
async def create_quota(quota: QuotaCreate):
    """
    Allocate a new fuel quota for a vehicle.
    Validates the vehicle's existence before creation.
    """
    # Validate vehicle existence
    if not ObjectId.is_valid(quota.vehicleId):
        raise HTTPException(status_code=400, detail="Invalid vehicleId format")
    
    vehicle = await vehicle_collection.find_one({"_id": ObjectId(quota.vehicleId)})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    quota_dict = quota.model_dump()
    result = await collection.insert_one(quota_dict)
    
    created_quota = await collection.find_one({"_id": result.inserted_id})
    created_quota["_id"] = str(created_quota["_id"])
    return created_quota

@router.get("/", 
            response_model=List[QuotaResponse],
            summary="List all quotas",
            tags=["Quotas"])
async def list_quotas():
    """
    Retrieve all fuel quota records.
    """
    quotas = await collection.find().to_list(100)
    for q in quotas:
        q["_id"] = str(q["_id"])
    return quotas

@router.get("/{id}", 
            response_model=QuotaResponse,
            summary="Get quota by ID",
            tags=["Quotas"])
async def get_quota(id: str):
    """
    Retrieve a specific quota record by its ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    quota = await collection.find_one({"_id": ObjectId(id)})
    if quota is None:
        raise HTTPException(status_code=404, detail=f"Quota with id {id} not found")
    
    quota["_id"] = str(quota["_id"])
    return quota

@router.put("/{id}", 
            response_model=QuotaResponse,
            summary="Update quota details",
            tags=["Quotas"])
async def update_quota(id: str, quota_update: QuotaUpdate):
    """
    Update an existing fuel quota record.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in quota_update.model_dump().items() if v is not None}
    
    if "vehicleId" in update_data:
        if not ObjectId.is_valid(update_data["vehicleId"]):
            raise HTTPException(status_code=400, detail="Invalid vehicleId format")
        vehicle = await vehicle_collection.find_one({"_id": ObjectId(update_data["vehicleId"])})
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")

    if len(update_data) >= 1:
        update_result = await collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Quota with id {id} not found")

    updated_quota = await collection.find_one({"_id": ObjectId(id)})
    updated_quota["_id"] = str(updated_quota["_id"])
    return updated_quota

@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a quota record",
               tags=["Quotas"])
async def delete_quota(id: str):
    """
    Remove a fuel quota record from the system.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Quota with id {id} not found")
    return None
