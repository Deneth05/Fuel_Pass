from fastapi import APIRouter, HTTPException, Depends
from models.transaction import Transaction, TransactionCreate, TransactionResponse
from database.mongo import get_database
from utils.external_services import (
    validate_vehicle, validate_fuel_stock, update_fuel_stock, 
    update_vehicle_quota, update_queue_status
)
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db=Depends(get_database)):
    # 1. Validate vehicle exists
    if not await validate_vehicle(transaction.vehicleId):
        raise HTTPException(status_code=400, detail="Vehicle not found in Citizen & Vehicle Service")

    # 2. Validate FuelStock is sufficient
    if not await validate_fuel_stock(transaction.stationId, transaction.fuelType, transaction.litersServed):
        raise HTTPException(status_code=400, detail="Insufficient Fuel Stock at station")

    # 3. Deduct consumed liters from FuelStock
    if not await update_fuel_stock(transaction.stationId, transaction.fuelType, transaction.litersServed):
        raise HTTPException(status_code=500, detail="Failed to update fuel stock")

    # 4. Deduct consumed liters from Quota
    if not await update_vehicle_quota(transaction.vehicleId, transaction.litersServed):
        # Rollback fuel stock if quota update fails (simplified rollback)
        await update_fuel_stock(transaction.stationId, transaction.fuelType, -transaction.litersServed)
        raise HTTPException(status_code=500, detail="Failed to update vehicle quota")

    # 5. Update Queue status to served if applicable
    await update_queue_status(transaction.vehicleId, transaction.stationId)

    # 6. Record Transaction
    transaction_data = transaction.model_dump()
    transaction_data["transactionTime"] = datetime.utcnow()
    
    result = await db.transactions.insert_one(transaction_data)
    transaction_data["_id"] = result.inserted_id
    
    return transaction_data

@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(db=Depends(get_database)):
    transactions = await db.transactions.find().to_list(1000)
    for t in transactions:
        t["_id"] = str(t["_id"])
    return transactions

@router.get("/{id}", response_model=TransactionResponse)
async def get_transaction(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid Transaction ID")
    
    transaction = await db.transactions.find_one({"_id": ObjectId(id)})
    if not transaction:
        raise HTTPException(status_code=414, detail="Transaction not found")
    
    transaction["_id"] = str(transaction["_id"])
    return transaction

@router.get("/station/{stationId}", response_model=List[TransactionResponse])
async def list_by_station(stationId: str, db=Depends(get_database)):
    transactions = await db.transactions.find({"stationId": stationId}).to_list(1000)
    for t in transactions:
        t["_id"] = str(t["_id"])
    return transactions

@router.get("/vehicle/{vehicleId}", response_model=List[TransactionResponse])
async def list_by_vehicle(vehicleId: str, db=Depends(get_database)):
    transactions = await db.transactions.find({"vehicleId": vehicleId}).to_list(1000)
    for t in transactions:
        t["_id"] = str(t["_id"])
    return transactions
