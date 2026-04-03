from fastapi import APIRouter, status, Request, Depends
from fastapi.security import HTTPBearer
from services.station_stock_services import FuelStockService
from models.stock import FuelStockResponse, FuelStockCreate, FuelStockUpdate, FuelStockDeduct
from utils.auth import role_required
from typing import List, Optional
from datetime import date

router = APIRouter()
service = FuelStockService()
security = HTTPBearer()

@router.post("/", 
             response_model=FuelStockResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create daily fuel stock",
             tags=["Fuel Stock"],
             dependencies=[Depends(role_required(["admin", "station_operator"])), Depends(security)])
async def create_fuel_stock(stock: FuelStockCreate, request: Request):
    return await service.create(stock.model_dump(mode="json"), request)

@router.get("/", 
            response_model=List[FuelStockResponse],
            summary="List fuel stock records",
            tags=["Fuel Stock"],
            dependencies=[Depends(security)])
async def list_fuel_stocks(request: Request, stationId: Optional[str] = None, date: Optional[date] = None):
    return await service.list_stocks(station_id=stationId, date=date.isoformat() if date else None, request=request)

@router.get("/{stock_id}", 
            response_model=FuelStockResponse,
            summary="Get stock record by ID",
            tags=["Fuel Stock"],
            dependencies=[Depends(security)])
async def get_fuel_stock(stock_id: str, request: Request):
    return await service.get_by_id(stock_id, request)

@router.put("/{stock_id}", 
            response_model=FuelStockResponse,
            summary="Update stock record",
            tags=["Fuel Stock"],
            dependencies=[Depends(role_required(["admin", "station_operator"])), Depends(security)])
async def update_fuel_stock(stock_id: str, stock_update: FuelStockUpdate, request: Request):
    return await service.update(stock_id, stock_update.model_dump(mode="json", exclude_none=True), request)

@router.delete("/{stock_id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete stock record",
               tags=["Fuel Stock"],
               dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def delete_fuel_stock(stock_id: str, request: Request):
    return await service.delete(stock_id, request)

@router.get("/station/{station_id}", 
            response_model=List[FuelStockResponse],
            summary="Get fuel stock for a station",
            tags=["Fuel Stock"],
            dependencies=[Depends(security)])
async def get_station_fuel_stock(station_id: str, request: Request):
    return await service.get_by_station(station_id, request)

@router.patch("/deduct", 
              response_model=FuelStockResponse,
              summary="Deduct fuel from stock",
              tags=["Fuel Stock"],
              dependencies=[Depends(role_required(["admin"])), Depends(security)])
async def deduct_fuel(payload: FuelStockDeduct, request: Request):
    return await service.deduct(payload.model_dump(mode="json"), request)
