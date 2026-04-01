from services.station_stock_services import StationService
from models.station import StationResponse
from typing import List

router = APIRouter()
service = StationService()

@router.get("/", 
            response_model=List[StationResponse],
            summary="List all fuel stations",
            tags=["Stations"])
async def get_stations():
    """
    Retrieve all fuel stations via the gateway.
    """

@router.get("/{station_id}", 
            response_model=StationResponse,
            summary="Get station by ID",
            tags=["Stations"])
async def get_station(station_id: str):
    """
    Retrieve details of a specific fuel station.
    """
