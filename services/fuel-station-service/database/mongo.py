import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fuel_pass_db")

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]


def get_database():
    # Motor DB handle is safe to reuse; FastAPI dependency will pass it through.
    return db

