from fastapi import APIRouter
from services.station_stock_services import FuelStockService
from models.stock import FuelStockResponse

router = APIRouter()
service = FuelStockService()

@router.get("/station/{station_id}", 
            response_model=FuelStockResponse,
            summary="Get fuel stock for a station",
            tags=["Fuel Stock"])
async def get_station_fuel_stock(station_id: str):
    """
    Check current fuel levels for a specific station via the gateway.
    """
    return await service.get_by_station(station_id)
