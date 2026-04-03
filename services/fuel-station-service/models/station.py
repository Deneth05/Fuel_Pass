from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic import field_validator


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class StationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Fuel Station - Downtown")
    location: str = Field(..., min_length=1, max_length=250, example="123 Main St, Springfield")
    fuelTypes: List[str] = Field(
        ...,
        min_length=1,
        example=["Petrol 92", "Diesel"],
        description="List of supported fuel type names at this station",
    )

    @field_validator("fuelTypes")
    @classmethod
    def normalize_fuel_types(cls, v: List[str]) -> List[str]:
        cleaned = [ft.strip() for ft in v if isinstance(ft, str) and ft.strip()]
        if not cleaned:
            raise ValueError("fuelTypes must contain at least one non-empty fuel type")
        # Remove duplicates while preserving order
        seen = set()
        out: List[str] = []
        for ft in cleaned:
            if ft not in seen:
                seen.add(ft)
                out.append(ft)
        return out


class StationCreate(StationBase):
    pass


class StationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="Updated Station Name")
    location: Optional[str] = Field(None, min_length=1, max_length=250, example="Updated location")
    fuelTypes: Optional[List[str]] = Field(
        None,
        min_length=1,
        example=["Petrol 95", "Diesel"],
    )

    @field_validator("fuelTypes")
    @classmethod
    def normalize_update_fuel_types(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is None:
            return None
        cleaned = [ft.strip() for ft in v if isinstance(ft, str) and ft.strip()]
        if not cleaned:
            raise ValueError("fuelTypes must contain at least one non-empty fuel type")
        seen = set()
        out: List[str] = []
        for ft in cleaned:
            if ft not in seen:
                seen.add(ft)
                out.append(ft)
        return out


class StationResponse(StationBase):
    id: str = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True)

