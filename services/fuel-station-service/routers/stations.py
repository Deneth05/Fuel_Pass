from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from database.mongo import get_database
from models.station import StationCreate, StationResponse, StationUpdate
from utils.auth import RoleChecker

# Shared role checkers
auth_admin = RoleChecker(["admin"])
auth_all = RoleChecker(["admin", "station_operator", "citizen"])


router = APIRouter()


@router.post(
    "/",
    response_model=StationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new station",
    tags=["Stations"],
    dependencies=[Depends(auth_admin)]
)
async def create_station(station: StationCreate, db=Depends(get_database)):
    station_dict = station.model_dump()

    result = await db["stations"].insert_one(station_dict)
    created = await db["stations"].find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created


@router.get(
    "/",
    response_model=List[StationResponse],
    summary="List stations",
    tags=["Stations"],
    dependencies=[Depends(auth_all)]
)
async def list_stations(db=Depends(get_database)):
    stations = await db["stations"].find().to_list(1000)
    for s in stations:
        s["_id"] = str(s["_id"])
    return stations


@router.get(
    "/{id}",
    response_model=StationResponse,
    summary="Get a station by ID",
    tags=["Stations"],
    dependencies=[Depends(auth_all)]
)
async def get_station(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid station ID format")

    station = await db["stations"].find_one({"_id": ObjectId(id)})
    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    station["_id"] = str(station["_id"])
    return station


@router.put(
    "/{id}",
    response_model=StationResponse,
    summary="Update a station by ID",
    tags=["Stations"],
    dependencies=[Depends(auth_admin)]
)
async def update_station(id: str, station_update: StationUpdate, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid station ID format")

    update_data = {k: v for k, v in station_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    result = await db["stations"].update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    updated = await db["stations"].find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return updated


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a station by ID",
    tags=["Stations"],
    dependencies=[Depends(auth_admin)]
)
async def delete_station(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid station ID format")

    result = await db["stations"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")
    return None

