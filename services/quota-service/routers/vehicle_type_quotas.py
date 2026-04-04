from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from bson import ObjectId
import logging
from database.mongo import get_database
from models.vehicle_type_quota import VehicleTypeQuotaCreate, VehicleTypeQuotaUpdate, VehicleTypeQuotaResponse
from models.vehicle_types import VehicleType
from utils.auth import RoleChecker

# Shared role checkers
auth_admin = RoleChecker(["admin"])
auth_staff = RoleChecker(["admin"])
auth_all = RoleChecker(["admin", "citizen"])

router = APIRouter()
db = get_database()
collection = db["vehicle_type_quotas"]

logger = logging.getLogger("quota-service")
logging.basicConfig(level=logging.INFO)

@router.post("/", 
             response_model=VehicleTypeQuotaResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Create a new vehicle type quota",
             tags=["Vehicle Type Quotas"],
             dependencies=[Depends(auth_admin)])
async def create_vehicle_type_quota(quota: VehicleTypeQuotaCreate):
    logger.info(f"Received request to create quota for: {quota.vehicleType}")
    existing = await collection.find_one({"vehicleType": quota.vehicleType.value if hasattr(quota.vehicleType, 'value') else quota.vehicleType})
    if existing:
        raise HTTPException(status_code=400, detail="Vehicle type quota already exists")

    quota_dict = quota.model_dump()
    result = await collection.insert_one(quota_dict)
    created = await collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created


@router.get("/", 
            response_model=List[VehicleTypeQuotaResponse],
            summary="List all vehicle type quotas",
            tags=["Vehicle Type Quotas"],
            dependencies=[Depends(auth_staff)])
async def list_vehicle_type_quotas():
    quotas = await collection.find().to_list(100)
    for q in quotas:
        q["_id"] = str(q["_id"])
    return quotas

@router.get("/{vehicle_type}", 
            response_model=VehicleTypeQuotaResponse,
            summary="Get quota for a specific vehicle type",
            tags=["Vehicle Type Quotas"],
            dependencies=[Depends(auth_all)])
async def get_vehicle_type_quota(vehicle_type: str):
    # Try searching by ID if it's a valid ObjectId
    if ObjectId.is_valid(vehicle_type):
        quota = await collection.find_one({"_id": ObjectId(vehicle_type)})
    else:
        # Otherwise search by vehicleType name
        quota = await collection.find_one({"vehicleType": vehicle_type})
        
    if not quota:
        raise HTTPException(status_code=404, detail=f"Quota for {vehicle_type} not found")
    quota["_id"] = str(quota["_id"])
    return quota

@router.put("/{vehicle_type}", 
            response_model=VehicleTypeQuotaResponse,
            summary="Update an existing vehicle type quota",
            tags=["Vehicle Type Quotas"],
            dependencies=[Depends(auth_admin)])
async def update_vehicle_type_quota(vehicle_type: str, quota_update: VehicleTypeQuotaUpdate):
    # Try finding by ID if it's a valid ObjectId
    if ObjectId.is_valid(vehicle_type):
        existing = await collection.find_one({"_id": ObjectId(vehicle_type)})
    else:
        # Otherwise search by vehicleType name
        existing = await collection.find_one({"vehicleType": vehicle_type})

    if not existing:
        raise HTTPException(status_code=404, detail=f"Quota for {vehicle_type} not found")
    
    update_data = {k: v for k, v in quota_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")
        
    await collection.update_one(
        {"_id": existing["_id"]},
        {"$set": update_data}
    )
    
    updated = await collection.find_one({"_id": existing["_id"]})
    updated["_id"] = str(updated["_id"])
    return updated

@router.delete("/{vehicle_type}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a vehicle type quota",
               tags=["Vehicle Type Quotas"],
               dependencies=[Depends(auth_admin)])
async def delete_vehicle_type_quota(vehicle_type: str):
    # Try deleting by ID if it's a valid ObjectId
    if ObjectId.is_valid(vehicle_type):
        result = await collection.delete_one({"_id": ObjectId(vehicle_type)})
    else:
        # Otherwise delete by vehicleType name
        result = await collection.delete_one({"vehicleType": vehicle_type})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Quota for {vehicle_type} not found")
    return None
