from fastapi import FastAPI
from routers import citizens, vehicles, quotas
from database.mongo import client

app = FastAPI(
    title="Citizen & Vehicle Service",
    description="""
    Microservice for managing Citizens, Vehicles, and Fuel Quotas in the Fuel Pass System.
    
    This service handles:
    * **Citizens**: Registration and management of personal details.
    * **Vehicles**: Linking vehicles to citizens and tracking fuel types.
    * **Quotas**: Allocating and tracking monthly fuel quotas for registered vehicles.
    """,
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(citizens.router, prefix="/citizens", tags=["Citizens"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(quotas.router, prefix="/quotas", tags=["Quotas"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Citizen & Vehicle Service API",
        "documentation": "/api-docs"
    }

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
