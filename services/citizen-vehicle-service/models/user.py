from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from utils.mongo_helper import PyObjectId

class UserBase(BaseModel):
    username: str = Field(..., description="Unique username", example="admin_user")
    role: str = Field(..., description="User role (system admin, user)", example="user")

class UserCreate(UserBase):
    password: str = Field(..., description="Plain text password", example="securepassword")

class UserLogin(BaseModel):
    username: str = Field(..., example="admin_user")
    password: str = Field(..., example="securepassword")

class UserResponse(UserBase):
    id: str = Field(alias="_id", description="Unique identifier")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
