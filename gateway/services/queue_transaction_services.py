from utils.helpers import forward_request

class QueueService:
    BASE_URL = "http://localhost:8003/queues"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def join_queue(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)
    
    async def get_by_station(self, station_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/station/{station_id}")
    
    async def update(self, queue_id: str, data: dict):
        return await forward_request("PUT", f"{self.BASE_URL}/{queue_id}", json=data)
    
    async def delete(self, queue_id: str):
        return await forward_request("DELETE", f"{self.BASE_URL}/{queue_id}")

class TransactionService:
    BASE_URL = "http://localhost:8004/transactions"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def get_by_id(self, transaction_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/{transaction_id}")

    async def get_by_station(self, station_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/station/{station_id}")

    async def get_by_vehicle(self, vehicle_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/vehicle/{vehicle_id}")

    async def create(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)

    async def update(self, transaction_id: str, data: dict):
        return await forward_request("PUT", f"{self.BASE_URL}/{transaction_id}", json=data)

    async def delete(self, transaction_id: str):
        return await forward_request("DELETE", f"{self.BASE_URL}/{transaction_id}")
