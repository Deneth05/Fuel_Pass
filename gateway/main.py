from fastapi import FastAPI
from routers import citizens, vehicles, quotas, stations, fuel_stock, queues, transactions, auth, vehicle_type_quotas

app = FastAPI(
    title="Fuel Pass API Gateway",
    description="""
    The API Gateway provides a unified entry point for all Fuel Pass system microservices.
    
    It integrates and documentation the following services:
    * **Citizen & Vehicle Service**: `Citizens`, `Vehicles`, and `Quotas`.
    * **Fuel Station Service**: `Stations` and `Fuel Stock`.
    * **Queue Service**: Managing pump `Queues`.
    * **Transaction Service**: Recording fuel `Transactions`.
    """,
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/redoc"
)

# Register routers
app.include_router(citizens.router, prefix="/citizens", tags=["Citizens"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(quotas.router, prefix="/quotas", tags=["Quotas"])
app.include_router(stations.router, prefix="/stations", tags=["Stations"])
app.include_router(fuel_stock.router, prefix="/fuel-stock", tags=["Fuel Stock"])
app.include_router(queues.router, prefix="/queues", tags=["Queues"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(vehicle_type_quotas.router, prefix="/vehicle-type-quotas", tags=["Vehicle Type Quotas"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Fuel Pass API Gateway",
        "documentation": "/api-docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
