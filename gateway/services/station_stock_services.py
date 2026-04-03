from utils.helpers import forward_request

from utils.helpers import forward_request

class StationService:
    BASE_URL = "http://localhost:8002/stations"
    
    async def create(self, station_data):
        return await forward_request("POST", f"{self.BASE_URL}/", data=station_data)
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def get_by_id(self, station_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/{station_id}")
    
    async def update(self, station_id: str, update_data):
        return await forward_request("PUT", f"{self.BASE_URL}/{station_id}", data=update_data)
    
    async def delete(self, station_id: str):
        return await forward_request("DELETE", f"{self.BASE_URL}/{station_id}")

class FuelStockService:
    BASE_URL = "http://localhost:8002/fuel-stock"
    
    async def create(self, stock_data):
        return await forward_request("POST", f"{self.BASE_URL}/", data=stock_data)
    
    async def list_stocks(self, station_id=None, date=None):
        params = {}
        if station_id: params["stationId"] = station_id
        if date: params["date"] = date
        return await forward_request("GET", f"{self.BASE_URL}/", params=params)
    
    async def get_by_id(self, stock_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/{stock_id}")
    
    async def update(self, stock_id: str, update_data):
        return await forward_request("PUT", f"{self.BASE_URL}/{stock_id}", data=update_data)
    
    async def delete(self, stock_id: str):
        return await forward_request("DELETE", f"{self.BASE_URL}/{stock_id}")
    
    async def get_by_station(self, station_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/station/{station_id}")
    
    async def deduct(self, deduct_data):
        return await forward_request("PATCH", f"{self.BASE_URL}/deduct", data=deduct_data)
