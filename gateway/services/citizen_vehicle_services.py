from utils.helpers import forward_request

class CitizenService:
    BASE_URL = "http://localhost:8001/citizens"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def get_by_id(self, citizen_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/{citizen_id}")
    
    async def create(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)

    async def update(self, citizen_id: str, data: dict):
        return await forward_request("PUT", f"{self.BASE_URL}/{citizen_id}", json=data)

    async def delete(self, citizen_id: str):
        return await forward_request("DELETE", f"{self.BASE_URL}/{citizen_id}")

class VehicleService:
    BASE_URL = "http://localhost:8001/vehicles"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")
    
    async def get_by_id(self, vehicle_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/{vehicle_id}")
    
    async def create(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)

    async def update(self, vehicle_id: str, data: dict):
        return await forward_request("PUT", f"{self.BASE_URL}/{vehicle_id}", json=data)

    async def delete(self, vehicle_id: str):
        return await forward_request("DELETE", f"{self.BASE_URL}/{vehicle_id}")

class QuotaService:
    BASE_URL = "http://localhost:8001/quotas"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")

    async def get_by_id(self, quota_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/{quota_id}")

    async def get_by_citizen(self, citizen_id: str):
        return await forward_request("GET", f"{self.BASE_URL}/citizen/{citizen_id}")

    async def create(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)

    async def update(self, quota_id: str, data: dict):
        return await forward_request("PUT", f"{self.BASE_URL}/{quota_id}", json=data)

    async def delete(self, quota_id: str):
        return await forward_request("DELETE", f"{self.BASE_URL}/{quota_id}")

    async def renew_all(self):
        return await forward_request("PUT", f"{self.BASE_URL}/renew-all")

class VehicleTypeQuotaService:
    BASE_URL = "http://localhost:8001/vehicle-type-quotas"
    
    async def get_all(self):
        return await forward_request("GET", f"{self.BASE_URL}/")

    async def get_by_type(self, vehicle_type: str):
        return await forward_request("GET", f"{self.BASE_URL}/{vehicle_type}")

    async def create_or_update(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data)

    async def update(self, vehicle_type: str, data: dict):
        return await forward_request("PUT", f"{self.BASE_URL}/{vehicle_type}", json=data)

    async def delete(self, vehicle_type: str):
        return await forward_request("DELETE", f"{self.BASE_URL}/{vehicle_type}")

class AuthService:
    BASE_URL = "http://localhost:8001/auth"
    
    async def login(self, data: dict):
        return await forward_request("POST", f"{self.BASE_URL}/login", json=data)
    
    async def logout(self, token: str):
        return await forward_request("POST", f"{self.BASE_URL}/logout", headers={"Authorization": f"Bearer {token}"})
