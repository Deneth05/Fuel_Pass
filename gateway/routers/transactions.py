from fastapi import APIRouter
from services.queue_transaction_services import TransactionService
from models.transaction import TransactionResponse, TransactionBase
from typing import List

router = APIRouter()
service = TransactionService()

@router.get("/", 
            response_model=List[TransactionResponse],
            summary="List all transactions",
            tags=["Transactions"])
async def get_transactions():
    """
    Retrieve history of fuel transactions via the gateway.
    """

@router.post("/", 
             response_model=TransactionResponse,
             summary="Create a new transaction",
             tags=["Transactions"])
async def create_transaction(transaction: TransactionBase):
    """
    Record a new fuel pumping transaction via the gateway.
    """
