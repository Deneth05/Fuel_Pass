from fastapi import APIRouter, Request, Depends
from services.citizen_vehicle_services import AuthService
from models.user import UserLogin
from models.citizen import CitizenCreate
from typing import Optional

router = APIRouter()
service = AuthService()

@router.post("/login", 
             summary="Login and receive JWT token",
             tags=["Authentication"])
async def login(credentials: UserLogin, request: Request):
    return await service.login(credentials.model_dump(), request)

@router.post("/logout",
             summary="Logout from the system",
             tags=["Authentication"])
async def logout(request: Request):
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header else ""
    return await service.logout(token, request)
