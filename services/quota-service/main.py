from fastapi import FastAPI
from routers import quotas, vehicle_type_quotas
from database.mongo import client

app = FastAPI(
    title="Quota Service",
    description="Microservice for managing fuel quotas and vehicle type quotas.",
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(quotas.router, prefix="/quotas", tags=["Quotas"])
app.include_router(vehicle_type_quotas.router, prefix="/vehicle-type-quotas", tags=["Vehicle Type Quotas"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Quota Service API",
        "documentation": "/api-docs"
    }

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=False)
