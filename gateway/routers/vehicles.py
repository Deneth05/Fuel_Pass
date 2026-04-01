from services.citizen_vehicle_services import VehicleService
from models.vehicle import VehicleResponse, VehicleCreate
from typing import List

router = APIRouter()
service = VehicleService()

@router.get("/", 
            response_model=List[VehicleResponse],
            summary="List all vehicles",
            tags=["Vehicles"])
async def get_vehicles():
    """
    Retrieve all registered vehicles via the gateway.
    """

@router.post("/", 
             response_model=VehicleResponse,
             summary="Register a new vehicle",
             tags=["Vehicles"])
async def create_vehicle(vehicle: VehicleCreate):
    """
    Register a vehicle for a citizen via the gateway.
    """
