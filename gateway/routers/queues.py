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

@router.post("/join", 
             response_model=QueueResponse,
             summary="Join a fuel queue",
             tags=["Queues"])
async def join_queue(data: QueueJoin):
    """
    Citizen joins a queue at a specific fuel station.
    """
