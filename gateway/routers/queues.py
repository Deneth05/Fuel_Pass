from fastapi import APIRouter, status, Request, Depends
from fastapi.security import HTTPBearer
from services.queue_transaction_services import QueueService
from models.queue import QueueResponse, QueueJoin, QueueUpdate
from utils.auth import role_required
from typing import List

router = APIRouter()
service = QueueService()
security = HTTPBearer()

@router.post("/", 
             response_model=QueueResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Join a fuel queue",
             tags=["Queues"],
             dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def join_queue(queue: QueueJoin, request: Request):
    return await service.join_queue(queue.model_dump(mode="json"), request)

@router.get("/", 
            response_model=List[QueueResponse],
            summary="List all queues",
            tags=["Queues"],
            dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def get_queues(request: Request):
    return await service.get_all(request)

@router.get("/{queue_id}", 
            response_model=QueueResponse,
            summary="Get queue by ID",
            tags=["Queues"],
            dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def get_queue(queue_id: str, request: Request):
    return await service.get_by_id(queue_id, request)

@router.get("/station/{station_id}", 
            response_model=List[QueueResponse],
            summary="List queues by station",
            tags=["Queues"],
            dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def get_by_station(station_id: str, request: Request):
    return await service.get_by_station(station_id, request)

@router.put("/{queue_id}", 
            response_model=QueueResponse,
            summary="Update queue status",
            tags=["Queues"],
            dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def update_queue(queue_id: str, queue_update: QueueUpdate, request: Request):
    return await service.update(queue_id, queue_update.model_dump(mode="json"), request)

@router.delete("/{queue_id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove from queue",
               tags=["Queues"],
               dependencies=[Depends(role_required(["admin", "citizen"])), Depends(security)])
async def delete_queue(queue_id: str, request: Request):
    return await service.delete(queue_id, request)
