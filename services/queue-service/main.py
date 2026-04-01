from fastapi import FastAPI
from routers import queue
from database.mongo import client

app = FastAPI(
    title="Queue Service",
    description="""
    Microservice for managing fuel station queues in the Fuel Pass System.
    
    This service handles:
    * **Queue Management**: CRUD for entries.
    * **Vehicle Validation**: Checks if vehicle exists and has enough quota via Citizen & Vehicle Service.
    * **Station Queues**: Sorted fetch of vehicles by join time.
    """,
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(queue.router, prefix="/queues", tags=["Queues"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Queue Service API",
        "documentation": "/api-docs"
    }

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    # Existing service uses port 8000, so we use 8001
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
