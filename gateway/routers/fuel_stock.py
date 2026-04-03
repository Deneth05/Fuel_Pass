from fastapi import APIRouter, status
from services.station_stock_services import FuelStockService
from models.stock import FuelStockResponse, FuelStockCreate, FuelStockUpdate, FuelStockDeduct
from typing import List, Optional
from datetime import date

router = APIRouter()
service = FuelStockService()

@router.post("/", 
             response_model=FuelStockResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create daily fuel stock",
             tags=["Fuel Stock"])
async def create_fuel_stock(stock: FuelStockCreate):
    """
    Initialize a new daily fuel stock record for a station.
    """
    return await service.create(stock.model_dump())

@router.get("/", 
            response_model=List[FuelStockResponse],
            summary="List fuel stock records",
            tags=["Fuel Stock"])
async def list_fuel_stocks(stationId: Optional[str] = None, date: Optional[date] = None):
    """
    List daily fuel stocks with optional filters.
    """
    return await service.list_stocks(station_id=stationId, date=date.isoformat() if date else None)

@router.get("/{stock_id}", 
            response_model=FuelStockResponse,
            summary="Get stock record by ID",
            tags=["Fuel Stock"])
async def get_fuel_stock(stock_id: str):
    """
    Get details of a specific daily fuel stock record.
    """
    return await service.get_by_id(stock_id)

@router.put("/{stock_id}", 
            response_model=FuelStockResponse,
            summary="Update stock record",
            tags=["Fuel Stock"])
async def update_fuel_stock(stock_id: str, stock_update: FuelStockUpdate):
    """
    Update an existing fuel stock record via the gateway.
    """
    return await service.update(stock_id, stock_update.model_dump(exclude_none=True))

@router.delete("/{stock_id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete stock record",
               tags=["Fuel Stock"])
async def delete_fuel_stock(stock_id: str):
    """
    Remove a fuel stock record.
    """
    return await service.delete(stock_id)

@router.get("/station/{station_id}", 
            response_model=List[FuelStockResponse],
            summary="Get fuel stock for a station",
            tags=["Fuel Stock"])
async def get_station_fuel_stock(station_id: str):
    """
    Check current fuel levels for a specific station via the gateway.
    """
    return await service.get_by_station(station_id)

@router.patch("/deduct", 
              response_model=FuelStockResponse,
              summary="Deduct fuel from stock",
              tags=["Fuel Stock"])
async def deduct_fuel(payload: FuelStockDeduct):
    """
    Deduct fuel from available liters (e.g., during a transaction).
    """
    return await service.deduct(payload.model_dump())
