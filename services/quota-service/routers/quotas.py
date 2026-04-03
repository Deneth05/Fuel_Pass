from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from bson import ObjectId
from database.mongo import get_database
from models.quota import QuotaCreate, QuotaUpdate, QuotaResponse
from utils.auth import RoleChecker

# Shared role checkers
auth_admin = RoleChecker(["admin"])
auth_citizen = RoleChecker(["citizen"])
auth_staff = RoleChecker(["admin"])
auth_all = RoleChecker(["admin", "citizen"])

router = APIRouter()
db = get_database()
collection = db["quotas"]
vehicle_collection = db["vehicles"] # Accessing vehicles for validation

@router.post("/", 
             response_model=QuotaResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Create a fuel quota",
             tags=["Quotas"],
             dependencies=[Depends(auth_admin)])
async def create_quota(quota: QuotaCreate):
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
            tags=["Quotas"],
            dependencies=[Depends(auth_admin)])
async def list_quotas():
    quotas = await collection.find().to_list(100)
    for q in quotas:
        q["_id"] = str(q["_id"])
    return quotas

@router.get("/{id}", 
            response_model=QuotaResponse,
            summary="Get quota by ID",
            tags=["Quotas"],
            dependencies=[Depends(auth_all)])
async def get_quota(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    quota = await collection.find_one({"_id": ObjectId(id)})
    if quota is None:
        raise HTTPException(status_code=404, detail=f"Quota with id {id} not found")
    
    quota["_id"] = str(quota["_id"])
    return quota

@router.get("/citizen/{citizen_id}", 
            response_model=QuotaResponse,
            summary="Get citizen quota",
            tags=["Quotas"],
            dependencies=[Depends(auth_all)])
async def get_citizen_quota(citizen_id: str):
    # Find vehicles for this citizen
    vehicles = await vehicle_collection.find({"citizenId": citizen_id}).to_list(1)
    if not vehicles:
        raise HTTPException(status_code=404, detail="No vehicles found for this citizen")
    
    latest_vehicle_id = str(vehicles[0]["_id"])
    quota = await collection.find_one({"vehicleId": latest_vehicle_id})
    if not quota:
         raise HTTPException(status_code=404, detail="Quota not found for the vehicle")
    
    quota["_id"] = str(quota["_id"])
    return quota

@router.put("/renew-all", 
            status_code=status.HTTP_200_OK,
            summary="Renew all vehicle quotas",
            tags=["Quotas"],
            dependencies=[Depends(auth_admin)])
async def renew_all_quotas():
    from utils.quota_manager import get_week_start_date
    from routers.vehicle_type_quotas import collection as type_quota_collection
    
    current_week_start = get_week_start_date()
    
    # Get all vehicles
    vehicles = await vehicle_collection.find().to_list(None)
    
    renewed_count = 0
    for vehicle in vehicles:
        vehicle_id = str(vehicle["_id"])
        vehicle_type = vehicle.get("vehicleType")
        
        # Get quota amount for this vehicle type
        type_quota = await type_quota_collection.find_one({"vehicleType": vehicle_type})
        allocated_liters = 0.0
        if type_quota:
            allocated_liters = type_quota["litersPerWeek"]
        
        # Check if a quota record already exists for this week
        existing_quota = await collection.find_one({
            "vehicleId": vehicle_id,
            "weekStartDate": current_week_start
        })
        
        if existing_quota:
            await collection.update_one(
                {"_id": existing_quota["_id"]},
                {"$set": {
                    "allocatedLiters": allocated_liters,
                    "consumedLiters": 0.0
                }}
            )
        else:
            new_quota = {
                "vehicleId": vehicle_id,
                "weekStartDate": current_week_start,
                "allocatedLiters": allocated_liters,
                "consumedLiters": 0.0
            }
            await collection.insert_one(new_quota)
        
        renewed_count += 1
        
    return {"message": f"Successfully renewed quotas for {renewed_count} vehicles", "weekStartDate": current_week_start}

@router.post("/vehicle/{vehicle_id}/deduct", 
             status_code=status.HTTP_200_OK,
             summary="Deduct from vehicle quota",
             tags=["Quotas"],
             dependencies=[Depends(auth_all)])
async def deduct_quota(vehicle_id: str, payload: dict):
    from utils.quota_manager import get_week_start_date
    
    amount = payload.get("amount")
    if amount is None or amount < 0:
        raise HTTPException(status_code=400, detail="Invalid deduction amount")

    current_week_start = get_week_start_date()
    
    quota = await collection.find_one({
        "vehicleId": vehicle_id,
        "weekStartDate": current_week_start
    })
    
    if not quota:
        raise HTTPException(status_code=404, detail=f"No quota record found for vehicle {vehicle_id} for the current week")

    remaining = quota["allocatedLiters"] - quota["consumedLiters"]
    if remaining < amount and amount > 0:
         raise HTTPException(status_code=400, detail=f"Insufficient quota. Available: {remaining}")

    result = await collection.update_one(
        {"_id": quota["_id"]},
        {"$inc": {"consumedLiters": amount}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update quota record")

    updated_quota = await collection.find_one({"_id": quota["_id"]})
    updated_quota["_id"] = str(updated_quota["_id"])
    return updated_quota

@router.put("/{id}", 
            response_model=QuotaResponse,
            summary="Update quota details",
            tags=["Quotas"],
            dependencies=[Depends(auth_admin)])
async def update_quota(id: str, quota_update: QuotaUpdate):
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
               tags=["Quotas"],
               dependencies=[Depends(auth_admin)])
async def delete_quota(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Quota with id {id} not found")
    return None
