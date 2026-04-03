from utils.helpers import forward_request
from fastapi import Request
from typing import Optional

class CitizenService:
    BASE_URL = "http://localhost:8001/citizens"
    
    async def get_all(self, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/", request=request)
    
    async def get_by_id(self, citizen_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/{citizen_id}", request=request)
    
    async def create(self, data: dict, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data, request=request)

    async def update(self, citizen_id: str, data: dict, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/{citizen_id}", json=data, request=request)

    async def delete(self, citizen_id: str, request: Optional[Request] = None):
        return await forward_request("DELETE", f"{self.BASE_URL}/{citizen_id}", request=request)

class VehicleService:
    BASE_URL = "http://localhost:8001/vehicles"
    
    async def get_all(self, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/", request=request)
    
    async def get_by_id(self, vehicle_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/{vehicle_id}", request=request)
    
    async def create(self, data: dict, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data, request=request)

    async def update(self, vehicle_id: str, data: dict, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/{vehicle_id}", json=data, request=request)

    async def delete(self, vehicle_id: str, request: Optional[Request] = None):
        return await forward_request("DELETE", f"{self.BASE_URL}/{vehicle_id}", request=request)

class QuotaService:
    BASE_URL = "http://localhost:8001/quotas"
    
    async def get_all(self, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/", request=request)

    async def get_by_id(self, quota_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/{quota_id}", request=request)

    async def get_by_citizen(self, citizen_id: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/citizen/{citizen_id}", request=request)

    async def create(self, data: dict, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data, request=request)

    async def update(self, quota_id: str, data: dict, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/{quota_id}", json=data, request=request)

    async def delete(self, quota_id: str, request: Optional[Request] = None):
        return await forward_request("DELETE", f"{self.BASE_URL}/{quota_id}", request=request)

    async def renew_all(self, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/renew-all", request=request)

class VehicleTypeQuotaService:
    BASE_URL = "http://localhost:8001/vehicle-type-quotas"
    
    async def get_all(self, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/", request=request)

    async def get_by_type(self, vehicle_type: str, request: Optional[Request] = None):
        return await forward_request("GET", f"{self.BASE_URL}/{vehicle_type}", request=request)

    async def create_or_update(self, data: dict, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/", json=data, request=request)

    async def update(self, vehicle_type: str, data: dict, request: Optional[Request] = None):
        return await forward_request("PUT", f"{self.BASE_URL}/{vehicle_type}", json=data, request=request)

    async def delete(self, vehicle_type: str, request: Optional[Request] = None):
        return await forward_request("DELETE", f"{self.BASE_URL}/{vehicle_type}", request=request)

class AuthService:
    BASE_URL = "http://localhost:8001/auth"
    
    async def login(self, data: dict, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/login", json=data, request=request)
    
    async def logout(self, token: str, request: Optional[Request] = None):
        return await forward_request("POST", f"{self.BASE_URL}/logout", headers={"Authorization": f"Bearer {token}"}, request=request)

    async def register(self, data: dict, request: Optional[Request] = None):
        # Forward registration to the citizen create endpoint in the microservice
        return await forward_request("POST", "http://localhost:8001/citizens/", json=data, request=request)
