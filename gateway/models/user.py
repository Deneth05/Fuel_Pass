from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    username: str = Field(..., description="Unique username (NIC for citizens)", example="123456789V")

class UserLogin(UserBase):
    password: str = Field(..., example="securepassword")

class UserResponse(UserBase):
    id: str = Field(alias="_id", description="Unique identifier")
    role: str = Field(..., description="User role", example="user")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
