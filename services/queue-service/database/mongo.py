import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Use the same MongoDB connection as the other services
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://isuripabasara2020_db_user:nmfR4dL9xVwBYPlx@cluster0.5umbqro.mongodb.net/?appName=Cluster0")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fuel_pass_db")

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

def get_database():
    return database

def get_collection(name: str):
    return database[name]
