from fastapi import APIRouter, HTTPException, status, Body
from typing import List
from datetime import datetime, timezone
from bson import ObjectId
from database.mongo import get_collection
from models.queue import QueueCreate, QueueUpdate, QueueResponse, QueueStatus
from utils.validation import validate_vehicle_and_quota

router = APIRouter()
collection = get_collection("queues")

@router.post("/", 
             response_model=QueueResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Add vehicle to queue")
async def add_to_queue(queue_data: QueueCreate):
    """
    Adds a vehicle to a queue at a station.
    Validates vehicle existence and fuel quota before adding.
    """
    # 1. Validate vehicle and quota from other microservice
    await validate_vehicle_and_quota(queue_data.vehicleId, queue_data.requestedLiters)
    
    # 2. Check if vehicle is already in an active queue (waiting status)
    existing = await collection.find_one({
        "vehicleId": queue_data.vehicleId,
        "status": QueueStatus.WAITING
    })
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Vehicle is already in a queue"
        )
    
    # 3. Create queue object
    queue_dict = queue_data.model_dump()
    queue_dict["status"] = QueueStatus.WAITING
    queue_dict["joinedAt"] = datetime.now(timezone.utc)
    
    result = await collection.insert_one(queue_dict)
    
    # 4. Fetch and return created entry
    created_entry = await collection.find_one({"_id": result.inserted_id})
    created_entry["_id"] = str(created_entry["_id"])
    return created_entry

@router.get("/", 
            response_model=List[QueueResponse],
            summary="List all queue entries")
async def list_queues():
    """
    Retrieve a list of all queue entries across all stations.
    """
    queues = await collection.find().to_list(100)
    for q in queues:
        q["_id"] = str(q["_id"])
    return queues

@router.get("/station/{stationId}", 
            response_model=List[QueueResponse],
            summary="Get queue for a station")
async def get_station_queue(stationId: str):
    """
    Retrieve the current queue for a specific station,
    sorted by joined time (earliest first).
    """
    queues = await collection.find({"stationId": stationId, "status": QueueStatus.WAITING}).sort("joinedAt", 1).to_list(100)
    for q in queues:
        q["_id"] = str(q["_id"])
    return queues

@router.get("/{id}", 
            response_model=QueueResponse,
            summary="Get queue entry by ID")
async def get_queue_entry(id: str):
    """
    Retrieve details of a specific queue entry by its ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    entry = await collection.find_one({"_id": ObjectId(id)})
    if not entry:
        raise HTTPException(status_code=404, detail="Queue entry not found")
    
    entry["_id"] = str(entry["_id"])
    return entry

@router.put("/{id}", 
            response_model=QueueResponse,
            summary="Update queue entry status or details")
async def update_queue_entry(id: str, update_data: QueueUpdate):
    """
    Update a queue entry (e.g., mark as served or cancelled, or update liters).
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="At least one field must be provided for update")
    
    result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Queue entry not found")
        
    updated_entry = await collection.find_one({"_id": ObjectId(id)})
    updated_entry["_id"] = str(updated_entry["_id"])
    return updated_entry

@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove entry from queue")
async def remove_from_queue(id: str):
    """
    Remove a specific entry from the system.
    Note: Usually, entries are cancelled instead of deleted for auditing.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Queue entry not found")
    
    return None
