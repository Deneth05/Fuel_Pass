import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path="d:/MTIT assignment 2/Fuel Pass/services/citizen-vehicle-service/.env")

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fuel_pass_db")

async def check_quota():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    vehicle_id = "69cfc539996d828241f358cd"
    print(f"Checking quota for vehicle: {vehicle_id}")
    
    # 1. Check vehicle
    vehicle = await db.vehicles.find_one({"_id": vehicle_id})
    if not vehicle:
        from bson import ObjectId
        vehicle = await db.vehicles.find_one({"_id": ObjectId(vehicle_id)})
    
    if vehicle:
        print(f"Vehicle found: {vehicle.get('registrationNumber')} - {vehicle.get('vehicleType')}")
    else:
        print("Vehicle NOT found in DB")
        return

    # 2. Check all quotas for this vehicle
    print("\nAll quotas for this vehicle:")
    async for q in db.quotas.find({"vehicleId": vehicle_id}):
        print(f"Quota: Week {q.get('weekStartDate')} | Allocated: {q.get('allocatedLiters')} | Consumed: {q.get('consumedLiters')}")

    # Also check with ObjectId
    print("\nChecking with ObjectId if needed...")
    async for q in db.quotas.find({"vehicleId": ObjectId(vehicle_id) if ObjectId.is_valid(vehicle_id) else vehicle_id}):
        print(f"Quota (ObjID): Week {q.get('weekStartDate')} | Allocated: {q.get('allocatedLiters')} | Consumed: {q.get('consumedLiters')}")

    client.close()

if __name__ == "__main__":
    asyncio.run(check_quota())
