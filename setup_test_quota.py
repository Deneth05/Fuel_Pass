import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="d:/MTIT assignment 2/Fuel Pass/services/citizen-vehicle-service/.env")

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fuel_pass_db")

async def setup_test_data():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    vehicle_id = "69cfc539996d828241f358cd"
    week_start = "2026-03-29"
    
    print(f"Ensuring quota for vehicle: {vehicle_id} for week {week_start}")
    
    # Insert quota
    quota = {
        "vehicleId": vehicle_id,
        "weekStartDate": week_start,
        "allocatedLiters": 20.0,
        "consumedLiters": 0.0
    }
    
    await db.quotas.delete_many({"vehicleId": vehicle_id, "weekStartDate": week_start})
    await db.quotas.insert_one(quota)
    print("Quota record inserted/reset.")

    client.close()

if __name__ == "__main__":
    asyncio.run(setup_test_data())
