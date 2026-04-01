from fastapi import APIRouter, Request, Depends
from services.citizen_vehicle_services import AuthService
from models.user import UserLogin
from typing import Optional

router = APIRouter()
service = AuthService()

@router.post("/login", 
             summary="Login and receive JWT token",
             tags=["Authentication"])
async def login(credentials: UserLogin):
    """
    Login via the gateway to receive a JWT access token.
    """
    return await service.login(credentials.model_dump())

@router.post("/logout",
             summary="Logout from the system",
             tags=["Authentication"])
async def logout(request: Request):
    """
    Logout via the gateway.
    """
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header else ""
    return await service.logout(token)
