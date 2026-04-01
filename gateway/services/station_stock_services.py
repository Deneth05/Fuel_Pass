from utils.helpers import forward_request

class StationService:
    BASE_URL = "http://localhost:8002/stations"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def get_by_id(self, station_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/{station_id}")

class FuelStockService:
    BASE_URL = "http://localhost:8002/fuel-stock"
    
    async def get_by_station(self, station_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/station/{station_id}")
