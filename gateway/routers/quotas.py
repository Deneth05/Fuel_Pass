from fastapi import APIRouter
from services.citizen_vehicle_services import QuotaService
from models.quota import QuotaResponse

router = APIRouter()
service = QuotaService()

@router.get("/citizen/{citizen_id}", 
            response_model=QuotaResponse,
            summary="Get citizen quota",
            tags=["Quotas"])
async def get_citizen_quota(citizen_id: str):
    """
    Retrieve quota details for a specific citizen's vehicle via the gateway.
    """
