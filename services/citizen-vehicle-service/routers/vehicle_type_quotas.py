from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from database.mongo import get_database
from models.vehicle_type_quota import VehicleTypeQuotaCreate, VehicleTypeQuotaUpdate, VehicleTypeQuotaResponse
from models.vehicle import VehicleType

router = APIRouter()
db = get_database()
collection = db["vehicle_type_quotas"]

@router.post("/", 
             response_model=VehicleTypeQuotaResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Create or update a vehicle type quota",
             tags=["Vehicle Type Quotas"])
async def create_vehicle_type_quota(quota: VehicleTypeQuotaCreate):
    """
    Define the fuel liters per week for a specific vehicle type.
    If it already exists, it updates it.
    """
    existing = await collection.find_one({"vehicleType": quota.vehicleType})
    if existing:
        await collection.update_one(
            {"_id": existing["_id"]},
            {"$set": {"litersPerWeek": quota.litersPerWeek}}
        )
        updated = await collection.find_one({"_id": existing["_id"]})
        updated["_id"] = str(updated["_id"])
        return updated

    quota_dict = quota.model_dump()
    result = await collection.insert_one(quota_dict)
    created = await collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created

@router.get("/", 
            response_model=List[VehicleTypeQuotaResponse],
            summary="List all vehicle type quotas",
            tags=["Vehicle Type Quotas"])
async def list_vehicle_type_quotas():
    quotas = await collection.find().to_list(100)
    for q in quotas:
        q["_id"] = str(q["_id"])
    return quotas

@router.get("/{vehicle_type}", 
            response_model=VehicleTypeQuotaResponse,
            summary="Get quota for a specific vehicle type",
            tags=["Vehicle Type Quotas"])
async def get_vehicle_type_quota(vehicle_type: VehicleType):
    quota = await collection.find_one({"vehicleType": vehicle_type})
    if not quota:
        raise HTTPException(status_code=404, detail=f"Quota for {vehicle_type} not found")
    quota["_id"] = str(quota["_id"])
    return quota
