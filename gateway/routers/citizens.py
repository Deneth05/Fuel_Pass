from services.citizen_vehicle_services import CitizenService
from models.citizen import CitizenResponse, CitizenCreate
from typing import List

router = APIRouter()
service = CitizenService()

@router.get("/", 
            response_model=List[CitizenResponse],
            summary="List all citizens",
            tags=["Citizens"])
async def get_citizens():
    """
    Retrieve all citizens through the gateway.
    """

@router.get("/{citizen_id}", 
            response_model=CitizenResponse,
            summary="Get citizen by ID",
            tags=["Citizens"])
async def get_citizen(citizen_id: str):
    """
    Retrieve a specific citizen's details via the gateway.
    """

@router.post("/", 
             response_model=CitizenResponse,
             summary="Create a new citizen",
             tags=["Citizens"])
async def create_citizen(citizen: CitizenCreate):
    """
    Register a new citizen via the gateway.
    """
