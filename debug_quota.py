import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    url = "mongodb+srv://isuripabasara2020_db_user:nmfR4dL9xVwBYPlx@cluster0.5umbqro.mongodb.net/?appName=Cluster0"
    client = AsyncIOMotorClient(url)
    db = client["fuel_pass_db"]
    vid = "69d0b4c10da910fd899a125d"
    
    quota = await db["quotas"].find_one({"vehicleId": vid})
    if quota:
        print(f"DEBUG_QUOTA: {quota}")
    else:
        print(f"DEBUG_QUOTA_NOT_FOUND: {vid}")

if __name__ == "__main__":
    asyncio.run(check())
