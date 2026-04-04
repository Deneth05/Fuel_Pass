from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from bson import ObjectId
import os
import httpx
from database.mongo import get_database
from models.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from utils.auth import RoleChecker

# Shared role checkers
auth_admin = RoleChecker(["admin"])
auth_citizen = RoleChecker(["citizen"])
auth_staff = RoleChecker(["admin"])
auth_all = RoleChecker(["admin", "citizen"])

router = APIRouter()
db = get_database()
collection = db["vehicles"]
citizen_collection = db["citizens"]

QUOTA_SERVICE_URL = os.getenv("QUOTA_SERVICE_URL", "http://127.0.0.1:8006")

@router.post("/", 
             response_model=VehicleResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Register a new vehicle",
             tags=["Vehicles"],
             dependencies=[Depends(auth_all)]) # Changed from open to auth_all to ensure we have a user context
async def create_vehicle(vehicle: VehicleCreate):
    """
    Register a vehicle for a citizen. 
    Validates the citizen's existence before registration.
    """
    # Validate citizen existence
    if not ObjectId.is_valid(vehicle.citizenId):
        raise HTTPException(status_code=400, detail="Invalid citizenId format")
    
    citizen = await citizen_collection.find_one({"_id": ObjectId(vehicle.citizenId)})
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")

    # Check if vehicle with the same number already exists
    existing_vehicle = await collection.find_one({"vehicleNumber": vehicle.vehicleNumber})
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Vehicle with this number already registered"
        )

    vehicle_dict = vehicle.model_dump()
    result = await collection.insert_one(vehicle_dict)
    vehicle_id = str(result.inserted_id)
    
    # Update citizen's registeredVehicles list
    await citizen_collection.update_one(
        {"_id": ObjectId(vehicle.citizenId)},
        {"$push": {"registeredVehicles": vehicle_id}}
    )

    # Auto-assign quota by calling Quota Service
    from utils.quota_manager import get_week_start_date
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Get quota amount for this vehicle type
            type_quota_resp = await client.get(f"{QUOTA_SERVICE_URL}/vehicle-type-quotas/{vehicle.vehicleType}")
            allocated_liters = 0.0
            if type_quota_resp.status_code == 200:
                allocated_liters = type_quota_resp.json().get("litersPerWeek", 0.0)
            
            # 2. Create initial quota record
            initial_quota = {
                "vehicleId": vehicle_id,
                "weekStartDate": get_week_start_date(),
                "allocatedLiters": allocated_liters,
                "consumedLiters": 0.0
            }
            await client.post(f"{QUOTA_SERVICE_URL}/quotas/", json=initial_quota)
    except Exception as e:
        # Log the error but don't fail vehicle creation
        import logging
        logging.error(f"Failed to auto-assign quota for vehicle {vehicle_id}: {str(e)}")
    
    created_vehicle = await collection.find_one({"_id": result.inserted_id})
    created_vehicle["_id"] = str(created_vehicle["_id"])
    return created_vehicle

@router.get("/", 
            response_model=List[VehicleResponse],
            summary="List all vehicles",
            tags=["Vehicles"],
            dependencies=[Depends(auth_admin)])
async def list_vehicles():
    """
    Retrieve a list of all registered vehicles.
    """
    vehicles = await collection.find().to_list(100)
    for v in vehicles:
        v["_id"] = str(v["_id"])
    return vehicles

@router.get("/{id}", 
            response_model=VehicleResponse,
            summary="Get vehicle by ID",
            tags=["Vehicles"],
            dependencies=[Depends(auth_all)])
async def get_vehicle(id: str):
    """
    Retrieve details of a specific vehicle by its ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    vehicle = await collection.find_one({"_id": ObjectId(id)})
    if vehicle is None:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {id} not found")
    
    vehicle["_id"] = str(vehicle["_id"])
    return vehicle

@router.put("/{id}", 
            response_model=VehicleResponse,
            summary="Update vehicle details",
            tags=["Vehicles"],
            dependencies=[Depends(auth_all)])
async def update_vehicle(id: str, vehicle_update: VehicleUpdate):
    """
    Update information for an existing vehicle.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in vehicle_update.model_dump().items() if v is not None}
    
    if "citizenId" in update_data:
        if not ObjectId.is_valid(update_data["citizenId"]):
             raise HTTPException(status_code=400, detail="Invalid citizenId format")
        citizen = await citizen_collection.find_one({"_id": ObjectId(update_data["citizenId"])})
        if not citizen:
            raise HTTPException(status_code=404, detail="Citizen not found")

    if len(update_data) >= 1:
        update_result = await collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Vehicle with id {id} not found")

    updated_vehicle = await collection.find_one({"_id": ObjectId(id)})
    updated_vehicle["_id"] = str(updated_vehicle["_id"])
    return updated_vehicle

@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a vehicle",
               tags=["Vehicles"],
               dependencies=[Depends(auth_admin)])
async def delete_vehicle(id: str):
    """
    Remove a vehicle from the system.
    Also removes the vehicle ID from the owner's registered vehicles list.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    vehicle = await collection.find_one({"_id": ObjectId(id)})
    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {id} not found")
        
    # Remove from citizen's list
    await citizen_collection.update_one(
        {"_id": ObjectId(vehicle["citizenId"])},
        {"$pull": {"registeredVehicles": id}}
    )

    await collection.delete_one({"_id": ObjectId(id)})
    return None
