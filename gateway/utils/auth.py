import os
import jwt
from typing import List, Optional
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your_super_secret_jwt_key_here")
ALGORITHM = "HS256"

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

from fastapi.responses import JSONResponse

async def auth_middleware(request: Request, call_next):
    # Public routes
    public_paths = [
        "/auth/login",
        "/stations/register",
        "/admin/register",
        "/api-docs",
        "/openapi.json",
        "/"
    ]
    
    path = request.url.path.rstrip("/")
    if not path: # Root path
        path = "/"
        
    if path in public_paths:
        return await call_next(request)

    # Citizen registration is public
    if path == "/citizens" and request.method == "POST":
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Authorization header missing"}
        )

    try:
        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if not payload:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )

        # Add user info to request state
        request.state.user_id = payload.get("sub")
        request.state.role = payload.get("role")
        request.state.nic = payload.get("nic")

        # Proceed with request
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Gateway Middleware Error: {str(e)}"}
        )

def role_required(allowed_roles: List[str]):
    def decorator(request: Request):
        user_role = getattr(request.state, "role", None)
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user_role}' not authorized"
            )
    return decorator
