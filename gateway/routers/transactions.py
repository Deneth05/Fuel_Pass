from fastapi import APIRouter, status, Request, Depends
from fastapi.security import HTTPBearer
from services.queue_transaction_services import TransactionService
from models.transaction import TransactionResponse, TransactionBase
from utils.auth import role_required
from typing import List

router = APIRouter()
service = TransactionService()
security = HTTPBearer()

@router.get("/", 
            response_model=List[TransactionResponse],
            summary="List all transactions",
            tags=["Transactions"],
            dependencies=[Depends(security), Depends(role_required(["admin"]))])
async def get_transactions(request: Request):
    return await service.get_all(request)

@router.get("/{id}", 
            response_model=TransactionResponse,
            summary="Get a transaction by ID",
            tags=["Transactions"],
            dependencies=[Depends(security), Depends(role_required(["admin", "citizen"]))])
async def get_transaction(id: str, request: Request):
    return await service.get_by_id(id, request)

@router.get("/station/{stationId}", 
            response_model=List[TransactionResponse],
            summary="List transactions by station",
            tags=["Transactions"],
            dependencies=[Depends(security), Depends(role_required(["admin"]))])
async def list_by_station(stationId: str, request: Request):
    return await service.get_by_station(stationId, request)

@router.get("/vehicle/{vehicleId}", 
            response_model=List[TransactionResponse],
            summary="List transactions by vehicle",
            tags=["Transactions"],
            dependencies=[Depends(security), Depends(role_required(["admin", "citizen"]))])
async def list_by_vehicle(vehicleId: str, request: Request):
    return await service.get_by_vehicle(vehicleId, request)

@router.post("/", 
             response_model=TransactionResponse,
             summary="Create a new transaction",
             tags=["Transactions"],
             dependencies=[Depends(security), Depends(role_required(["admin"]))])
async def create_transaction(transaction: TransactionBase, request: Request):
    return await service.create(transaction.model_dump(mode="json"), request)

@router.put("/{id}", 
            response_model=TransactionResponse,
            summary="Update a transaction",
            tags=["Transactions"],
            dependencies=[Depends(security), Depends(role_required(["admin"]))])
async def update_transaction(id: str, transaction: TransactionBase, request: Request):
    return await service.update(id, transaction.model_dump(mode="json"), request)

@router.delete("/{id}", 
               summary="Delete a transaction",
               tags=["Transactions"],
               dependencies=[Depends(security), Depends(role_required(["admin"]))])
async def delete_transaction(id: str, request: Request):
    return await service.delete(id, request)
