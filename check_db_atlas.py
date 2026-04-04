import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def check_db():
    # Use the Atlas URL from quota-service/.env
    url = "mongodb+srv://isuripabasara2020_db_user:nmfR4dL9xVwBYPlx@cluster0.5umbqro.mongodb.net/?appName=Cluster0"
    client = AsyncIOMotorClient(url)
    db = client["fuel_pass_db"]
    
    vehicle_id_str = "69d0b4c10da910fd899a125d"
    
    print(f"Checking Quotas for vehicleId: {vehicle_id_str}")
    
    # Check for string vehicleId
    cursor = db["quotas"].find({"vehicleId": vehicle_id_str})
    async for doc in cursor:
        print(f"Found (string ID): {doc}")
        
    # Check for ObjectId vehicleId
    if ObjectId.is_valid(vehicle_id_str):
        cursor = db["quotas"].find({"vehicleId": ObjectId(vehicle_id_str)})
        async for doc in cursor:
            print(f"Found (ObjectId): {doc}")

    # Check vehicle existence
    vehicle = await db["vehicles"].find_one({"_id": ObjectId(vehicle_id_str)})
    print(f"Vehicle Object: {vehicle}")

    # Check current week start date logic
    from datetime import datetime, timedelta
    dt = datetime.now()
    days_since_sunday = (dt.weekday() + 1) % 7
    sunday = dt - timedelta(days=days_since_sunday)
    expected_week_start = sunday.strftime("%Y-%m-%d")
    print(f"Current server expected week start: {expected_week_start}")

if __name__ == "__main__":
    asyncio.run(check_db())
