from fastapi import APIRouter, HTTPException, status, Depends
from database.mongo import get_database
from models.user import UserCreate, UserLogin, UserResponse
from utils.auth import get_password_hash, verify_password, create_access_token, get_current_user
from datetime import timedelta

router = APIRouter()
db = get_database()
collection = db["users"]

@router.post("/login", 
             summary="Login and receive JWT token",
             tags=["Authentication"])
async def login(credentials: UserLogin):
    user = await collection.find_one({"username": credentials.username})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout",
             summary="Logout (client-side implementation)",
             tags=["Authentication"])
async def logout(user: dict = Depends(get_current_user)):
    """
    JWT is stateless. Client simply discards the token.
    This endpoint confirms the action.
    """
    return {"message": "Successfully logged out"}
