from utils.helpers import forward_request
from fastapi import Request
from typing import Optional

class QueueService:
    BASE_URL = "http://127.0.0.1:8003/queues"
    
    async def get_all(self, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/", request=request)
    
    async def join_queue(self, data: dict, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data, request=request)
    
    async def get_by_station(self, station_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/station/{station_id}", request=request)
    
    async def update(self, queue_id: str, data: dict, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/{queue_id}", json=data, request=request)
    
    async def delete(self, queue_id: str, request: Optional[Request] = None):
        return await forward_request("DELETE", f"{self.BASE_URL}/{queue_id}", request=request)

class TransactionService:
    BASE_URL = "http://127.0.0.1:8004/transactions"
    
    async def get_all(self, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/", request=request)
    
    async def get_by_id(self, transaction_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/{transaction_id}", request=request)

    async def get_by_station(self, station_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/station/{station_id}", request=request)

    async def get_by_vehicle(self, vehicle_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/vehicle/{vehicle_id}", request=request)

    async def create(self, data: dict, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data, request=request)

    async def update(self, transaction_id: str, data: dict, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/{transaction_id}", json=data, request=request)

    async def delete(self, transaction_id: str, request: Optional[Request] = None):
        return await forward_request("DELETE", f"{self.BASE_URL}/{transaction_id}", request=request)
