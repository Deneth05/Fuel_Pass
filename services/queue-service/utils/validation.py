import os
import httpx
from fastapi import HTTPException, status

CITIZEN_VEHICLE_SERVICE_URL = os.getenv("CITIZEN_VEHICLE_SERVICE_URL", "http://localhost:8000")

async def validate_vehicle_and_quota(vehicle_id: str, requested_liters: float):
    """
    Validates if the vehicle exists and has enough fuel quota.
    Calls the Citizen & Vehicle Service.
    """
    async with httpx.AsyncClient() as client:
        # 1. Check if vehicle exists
        try:
            vehicle_response = await client.get(f"{CITIZEN_VEHICLE_SERVICE_URL}/vehicles/{vehicle_id}")
            if vehicle_response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Vehicle with ID {vehicle_id} not found in Citizen & Vehicle Service"
                )
            vehicle_response.raise_for_status()
            vehicle_data = vehicle_response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to reach Citizen & Vehicle Service: {str(e)}"
            )

        # 2. Check if quota is sufficient
        # In a real scenario, there might be a specific endpoint for this.
        # Based on the requirement, we check if vehicle quota is sufficient.
        # Assuming the vehicle object or a separate quota endpoint provides this.
        # Let's check the quota endpoint if it exists in citizen-vehicle-service.
        
        try:
            # Reusing the logic from the existing service's expected structure
            quota_response = await client.get(f"{CITIZEN_VEHICLE_SERVICE_URL}/quotas/vehicle/{vehicle_id}")
            if quota_response.status_code == 404:
                 # If no specific quota record, maybe it's not allocated
                 raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fuel quota allocated for this vehicle"
                )
            quota_response.raise_for_status()
            quota_data = quota_response.json()
            
            available_liters = quota_data.get("remainingLiters", 0)
            if requested_liters > available_liters:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient fuel quota. Requested: {requested_liters}L, Available: {available_liters}L"
                )
        except httpx.HTTPStatusError as e:
             if e.response.status_code != 404:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Error checking quota: {str(e)}"
                )
             else:
                 raise HTTPException(status_code=400, detail="Quota information not found for vehicle")
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to reach Citizen & Vehicle Service for quota check: {str(e)}"
            )

    return True
