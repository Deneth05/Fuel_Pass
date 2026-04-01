from utils.helpers import forward_request

class QueueService:
    BASE_URL = "http://localhost:8003/queues"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def join_queue(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/join", json=data)

class TransactionService:
    BASE_URL = "http://localhost:8004/transactions"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def create(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)
