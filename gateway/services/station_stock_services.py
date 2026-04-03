from utils.helpers import forward_request
from fastapi import Request
from typing import Optional

class StationService:
    BASE_URL = "http://localhost:8002/stations"
    
    async def create(self, station_data, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/", json=station_data, request=request)
    
    async def get_all(self, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/", request=request)
    
    async def get_by_id(self, station_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/{station_id}", request=request)
    
    async def update(self, station_id: str, update_data, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/{station_id}", json=update_data, request=request)
    
    async def delete(self, station_id: str, request: Optional[Request] = None):
        return await forward_request("DELETE", f"{self.BASE_URL}/{station_id}", request=request)

class FuelStockService:
    BASE_URL = "http://localhost:8002/fuel-stock"
    
    async def create(self, stock_data, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/", json=stock_data, request=request)
    
    async def list_stocks(self, station_id=None, date=None, request: Optional[Request] = None):
        params = {}
        if station_id: params["stationId"] = station_id
        if date: params["date"] = date
        return await forward_request("GET", f"{self.BASE_URL}/", params=params, request=request)
    
    async def get_by_id(self, stock_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/{stock_id}", request=request)
    
    async def update(self, stock_id: str, update_data, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/{stock_id}", json=update_data, request=request)
    
    async def delete(self, stock_id: str, request: Optional[Request] = None):
        return await forward_request("DELETE", f"{self.BASE_URL}/{stock_id}", request=request)
    
    async def get_by_station(self, station_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/station/{station_id}", request=request)
    
    async def deduct(self, deduct_data, request: Optional[Request] = None):
        return await forward_request("PATCH", f"{self.BASE_URL}/deduct", json=deduct_data, request=request)
