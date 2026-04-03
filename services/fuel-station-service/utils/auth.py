import os
from typing import List, Optional
from fastapi import Depends, HTTPException, status, Header
from dotenv import load_dotenv

load_dotenv()

# For Microservices: Trust forwarded headers from Gateway
def get_current_user(
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    x_user_role: Optional[str] = Header(None, alias="X-User-Role"),
    x_user_nic: Optional[str] = Header(None, alias="X-User-NIC")
):
    if not x_user_id or not x_user_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity headers missing"
        )
    return {
        "user_id": x_user_id,
        "role": x_user_role,
        "nic": x_user_nic
    }

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(get_current_user)):
        if user["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user['role']}' not authorized"
            )
        return user
