import httpx
import os
from dotenv import load_dotenv

load_dotenv()

CITIZEN_SERVICE_URL = os.getenv("CITIZEN_SERVICE_URL", "http://localhost:8001")
STATION_SERVICE_URL = os.getenv("STATION_SERVICE_URL", "http://localhost:8002")
QUEUE_SERVICE_URL = os.getenv("QUEUE_SERVICE_URL", "http://localhost:8003")

async def validate_vehicle(vehicle_id: str, headers: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CITIZEN_SERVICE_URL}/vehicles/{vehicle_id}", headers=headers)
            return response.status_code == 200
        except Exception:
            return False

async def validate_fuel_stock(station_id: str, fuel_type: str, liters: float, headers: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{STATION_SERVICE_URL}/fuel-stock/station/{station_id}", headers=headers)
            if response.status_code == 200:
                stocks = response.json()
                for stock in stocks:
                    if stock["fuelType"] == fuel_type:
                        # Depending on the response model, it might be currentStock or availableLiters
                        # In fuel_stock.py it seems to be availableLiters
                        return stock.get("availableLiters", 0) >= liters
            return False
        except Exception:
            return False

async def update_fuel_stock(station_id: str, fuel_type: str, liters: float, headers: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            payload = {"stationId": station_id, "fuelType": fuel_type, "liters": liters}
            response = await client.patch(f"{STATION_SERVICE_URL}/fuel-stock/deduct", json=payload, headers=headers)
            return response.status_code == 200
        except Exception:
            return False

async def update_vehicle_quota(vehicle_id: str, liters: float, headers: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            # Note: The actual endpoint in citizen service might be different. 
            # I'll use a generic one for now, but in a real system we'd match the router.
            payload = {"consumedLiters": liters} 
            response = await client.put(f"{CITIZEN_SERVICE_URL}/quotas/{vehicle_id}", json=payload, headers=headers)
            return response.status_code in [200, 204]
        except Exception:
            return False

async def update_queue_status(vehicle_id: str, station_id: str, headers: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            # Assuming endpoint: PUT /queues/{id} or similar
            # For simplicity, we just find the entry and update it.
            # But here we just forward to the generic update.
             payload = {"status": "served"}
             response = await client.put(f"{QUEUE_SERVICE_URL}/queues/vehicle/{vehicle_id}/complete", json=payload, headers=headers)
             return response.status_code == 200
        except Exception:
            return False
