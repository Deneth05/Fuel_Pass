from utils.helpers import forward_request

class CitizenService:
    BASE_URL = "http://localhost:8001/citizens"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def get_by_id(self, citizen_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/{citizen_id}")
    
    async def create(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)

class VehicleService:
    BASE_URL = "http://localhost:8001/vehicles"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def create(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)

class QuotaService:
    BASE_URL = "http://localhost:8001/quotas"
    
    async def get_by_citizen(self, citizen_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/citizen/{citizen_id}")
