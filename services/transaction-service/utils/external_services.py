import httpx
import os
from dotenv import load_dotenv

load_dotenv()

CITIZEN_SERVICE_URL = os.getenv("CITIZEN_SERVICE_URL", "http://localhost:8001")
STATION_SERVICE_URL = os.getenv("STATION_SERVICE_URL", "http://localhost:8002")
QUEUE_SERVICE_URL = os.getenv("QUEUE_SERVICE_URL", "http://localhost:8003")

async def validate_vehicle(vehicle_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CITIZEN_SERVICE_URL}/vehicles/{vehicle_id}")
            return response.status_code == 200
        except Exception:
            return False

async def validate_fuel_stock(station_id: str, fuel_type: str, liters: float):
    async with httpx.AsyncClient() as client:
        try:
            # Assuming endpoint: GET /fuel-stock/station/{station_id} returns list of stocks
            response = await client.get(f"{STATION_SERVICE_URL}/fuel-stock/station/{station_id}")
            if response.status_code == 200:
                stocks = response.json()
                for stock in stocks:
                    if stock["fuelType"] == fuel_type:
                        return stock["currentStock"] >= liters
            return False
        except Exception:
            return False

async def update_fuel_stock(station_id: str, fuel_type: str, liters: float):
    async with httpx.AsyncClient() as client:
        try:
            # Assuming endpoint: PATCH /fuel-stock/deduct
            payload = {"stationId": station_id, "fuelType": fuel_type, "liters": liters}
            response = await client.patch(f"{STATION_SERVICE_URL}/fuel-stock/deduct", json=payload)
            return response.status_code == 200
        except Exception:
            return False

async def update_vehicle_quota(vehicle_id: str, liters: float):
    async with httpx.AsyncClient() as client:
        try:
            # Assuming endpoint: PATCH /quotas/deduct/{vehicle_id}
            payload = {"liters": liters}
            response = await client.patch(f"{CITIZEN_SERVICE_URL}/quotas/deduct/{vehicle_id}", json=payload)
            return response.status_code == 200
        except Exception:
            return False

async def update_queue_status(vehicle_id: str, station_id: str):
    async with httpx.AsyncClient() as client:
        try:
            # Assuming endpoint: PATCH /queues/serve/{vehicle_id}
            payload = {"stationId": station_id}
            response = await client.patch(f"{QUEUE_SERVICE_URL}/queues/serve/{vehicle_id}", json=payload)
            return response.status_code == 200
        except Exception:
            return False
