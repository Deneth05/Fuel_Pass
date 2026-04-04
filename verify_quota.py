import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def verify():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["fuel_pass_db"]
    
    vehicle_id = "69d0af9768e0622b4151807d"
    
    # 1. Check vehicle
    vehicle = await db["vehicles"].find_one({"_id": vehicle_id})
    if not vehicle:
        # Try as ObjectId
        from bson import ObjectId
        vehicle = await db["vehicles"].find_one({"_id": ObjectId(vehicle_id)})
    
    if vehicle:
        print(f"Vehicle found: {vehicle.get('vehicleType')}")
    else:
        print("Vehicle NOT found")
        return

    # 2. Check quota
    quota = await db["quotas"].find_one({"vehicleId": vehicle_id})
    if not quota:
         # Check if stored as string or ObjectId
         quota = await db["quotas"].find_one({"vehicleId": str(vehicle_id)})
         
    if quota:
        print(f"Quota found: Allocated={quota.get('allocatedLiters')}, Consumed={quota.get('consumedLiters')}, Week={quota.get('weekStartDate')}")
    else:
        print("Quota NOT found for this vehicle")

    # 3. List all quotas just to see
    quotas = await db["quotas"].find().to_list(10)
    print(f"Total quotas found: {len(quotas)}")
    for q in quotas:
        print(f"Vehicle: {q.get('vehicleId')}, Allocated: {q.get('allocatedLiters')}")

    # 4. List all vehicle type quotas
    vt_quotas = await db["vehicle_type_quotas"].find().to_list(10)
    print(f"Total vehicle type quotas: {len(vt_quotas)}")
    for vt in vt_quotas:
        print(f"Type: {vt.get('vehicleType')}, Liters: {vt.get('litersPerWeek')}")

if __name__ == "__main__":
    asyncio.run(verify())
