from fastapi import APIRouter
from services.queue_transaction_services import QueueService
from models.queue import QueueResponse, QueueJoin
from typing import List

router = APIRouter()
service = QueueService()

@router.get("/", 
            response_model=List[QueueResponse],
            summary="List all active queues",
            tags=["Queues"])
async def get_queues():
    """
    Retrieve information about all current fuel pump queues.
    """
    return await service.get_all()

@router.post("/", 
             response_model=QueueResponse,
             summary="Join a fuel queue",
             tags=["Queues"])
async def join_queue(data: QueueJoin):
    """
    Citizen joins a queue at a specific fuel station.
    """
    return await service.join_queue(data.model_dump())

@router.get("/station/{stationId}", 
            response_model=List[QueueResponse],
            summary="Get queue for a station",
            tags=["Queues"])
async def get_station_queue(stationId: str):
    """
    Retrieve the current queue for a specific station.
    """
    return await service.get_by_station(stationId)

@router.put("/{id}", 
            response_model=QueueResponse,
            summary="Update queue entry",
            tags=["Queues"])
async def update_queue_entry(id: str, data: dict): # Use dict for partial updates via gateway
    """
    Update a queue entry (e.g., mark as served or cancelled).
    """
    return await service.update(id, data)

@router.delete("/{id}", 
               summary="Remove from queue",
               tags=["Queues"])
async def delete_queue_entry(id: str):
    """
    Remove a specific entry from the queue.
    """
    return await service.delete(id)
