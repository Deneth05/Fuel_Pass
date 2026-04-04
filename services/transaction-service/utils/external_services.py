import httpx
import os
from dotenv import load_dotenv

load_dotenv()

CITIZEN_SERVICE_URL = os.getenv("CITIZEN_SERVICE_URL", "http://127.0.0.1:8001")
QUOTA_SERVICE_URL = os.getenv("QUOTA_SERVICE_URL", "http://127.0.0.1:8006")
STATION_SERVICE_URL = os.getenv("STATION_SERVICE_URL", "http://127.0.0.1:8002")
QUEUE_SERVICE_URL = os.getenv("QUEUE_SERVICE_URL", "http://127.0.0.1:8003")

async def validate_vehicle(vehicle_id: str, headers: dict = None):
    async with httpx.AsyncClient(trust_env=False, timeout=20.0) as client:
        try:
            response = await client.get(f"{CITIZEN_SERVICE_URL}/vehicles/{vehicle_id}", headers=headers)
            return response.status_code == 200
        except Exception:
            return False

async def validate_fuel_stock(station_id: str, fuel_type: str, liters: float, headers: dict = None):
    async with httpx.AsyncClient(trust_env=False, timeout=20.0) as client:
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
    async with httpx.AsyncClient(trust_env=False, timeout=20.0) as client:
        try:
            payload = {"stationId": station_id, "fuelType": fuel_type, "liters": liters}
            response = await client.patch(f"{STATION_SERVICE_URL}/fuel-stock/deduct", json=payload, headers=headers)
            return response.status_code == 200
        except Exception:
            return False

async def update_vehicle_quota(vehicle_id: str, liters: float, headers: dict = None):
    async with httpx.AsyncClient(trust_env=False, timeout=20.0) as client:
        try:
            payload = {"amount": liters} 
            url = f"{QUOTA_SERVICE_URL}/quotas/vehicle/{vehicle_id}/deduct"
            print(f"DEBUG: Calling {url} with {payload}")
            response = await client.post(url, json=payload, headers=headers)
            print(f"DEBUG: Response from citizen-service: {response.status_code} - {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"DEBUG: update_vehicle_quota exception: {e}")
            return False

async def update_queue_status(vehicle_id: str, station_id: str, headers: dict = None):
    async with httpx.AsyncClient(trust_env=False, timeout=20.0) as client:
        try:
            # Assuming endpoint: PUT /queues/{id} or similar
            # For simplicity, we just find the entry and update it.
            # But here we just forward to the generic update.
             payload = {"status": "served"}
             response = await client.put(f"{QUEUE_SERVICE_URL}/queues/vehicle/{vehicle_id}/complete", json=payload, headers=headers)
             return response.status_code == 200
        except Exception:
            return False
