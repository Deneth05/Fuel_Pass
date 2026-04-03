from fastapi import FastAPI
import os
from dotenv import load_dotenv

from routers import stations, fuel_stock
from database.mongo import client

load_dotenv()

app = FastAPI(
    title="Fuel Station Service",
    description="""
    Microservice for managing fuel stations and daily fuel stock.

    This service handles:
    * **Stations CRUD**: Create/read/update/delete stations with their supported fuel types.
    * **FuelStock CRUD**: Create/read/update/delete daily fuel stock per station and fuel type.
    * **FuelStock Deduction** (optional): Deduct available liters for a given day and fuel type.
    """,
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/redoc",
)

app.include_router(stations.router, prefix="/stations", tags=["Stations"])
app.include_router(fuel_stock.router, prefix="/fuel-stock", tags=["FuelStock"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Fuel Station Service API",
        "documentation": "/api-docs",
    }


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8002))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

