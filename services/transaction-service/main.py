from fastapi import FastAPI
from routers import transactions
from database.mongo import client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Transaction Service",
    description="""
    Microservice for managing fuel pumping transactions in the Fuel Pass System.
    
    This service handles:
    * **Transaction CRUD**: Recording and retrieving fuel transactions.
    * **Inter-service Validation**: Verification of vehicle existence and fuel availability.
    * **Automated Updates**: Deducting fuel from stock and quotas upon transaction success.
    """,
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Transaction Service API",
        "documentation": "/api-docs"
    }

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8004))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
