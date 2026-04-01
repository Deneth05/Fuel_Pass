from fastapi import APIRouter
from services.queue_transaction_services import TransactionService
from models.transaction import TransactionResponse, TransactionBase
from typing import List

router = APIRouter()
service = TransactionService()

@router.get("/", 
            response_model=List[TransactionResponse],
            summary="List all transactions",
            tags=["Transactions"])
async def get_transactions():
    """
    Retrieve history of fuel transactions via the gateway.
    """
    return await service.get_all()

@router.get("/{id}", 
            response_model=TransactionResponse,
            summary="Get a transaction by ID",
            tags=["Transactions"])
async def get_transaction(id: str):
    """
    Retrieve a specific fuel transaction by its ID via the gateway.
    """
    return await service.get_by_id(id)

@router.get("/station/{stationId}", 
            response_model=List[TransactionResponse],
            summary="List transactions by station",
            tags=["Transactions"])
async def list_by_station(stationId: str):
    """
    Retrieve history of fuel transactions for a specific station via the gateway.
    """
    return await service.get_by_station(stationId)

@router.get("/vehicle/{vehicleId}", 
            response_model=List[TransactionResponse],
            summary="List transactions by vehicle",
            tags=["Transactions"])
async def list_by_vehicle(vehicleId: str):
    """
    Retrieve history of fuel transactions for a specific vehicle via the gateway.
    """
    return await service.get_by_vehicle(vehicleId)

@router.post("/", 
             response_model=TransactionResponse,
             summary="Create a new transaction",
             tags=["Transactions"])
async def create_transaction(transaction: TransactionBase):
    """
    Record a new fuel pumping transaction via the gateway.
    """
    return await service.create(transaction.model_dump())

@router.put("/{id}", 
            response_model=TransactionResponse,
            summary="Update a transaction",
            tags=["Transactions"])
async def update_transaction(id: str, transaction: TransactionBase):
    """
    Update an existing fuel transaction via the gateway.
    """
    return await service.update(id, transaction.model_dump())

@router.delete("/{id}", 
               summary="Delete a transaction",
               tags=["Transactions"])
async def delete_transaction(id: str):
    """
    Delete a fuel transaction record via the gateway.
    """
    return await service.delete(id)
