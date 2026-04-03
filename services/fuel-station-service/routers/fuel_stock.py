from __future__ import annotations

from datetime import date
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from database.mongo import get_database
from models.fuel_stock import (
    FuelStockCreate,
    FuelStockDeduct,
    FuelStockResponse,
    FuelStockUpdate,
)
from utils.validation import (
    find_station,
    fuel_type_supported,
    object_id_or_raise,
    utc_today_date,
)


router = APIRouter()


@router.post(
    "/",
    response_model=FuelStockResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create daily fuel stock for a station and fuel type",
)
async def create_fuel_stock(payload: FuelStockCreate, db=Depends(get_database)):
    # Validate station exists and supports this fuel type
    try:
        station = await find_station(db, payload.stationId)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not station:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid stationId")

    fuel_type = payload.fuelType
    if not fuel_type_supported(station, fuel_type):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fuelType is not supported by this station")

    # Normalize into DB-friendly shape
    available = payload.availableLiters if payload.availableLiters is not None else payload.receivedLiters
    stock_dict = payload.model_dump()
    stock_dict["availableLiters"] = available
    stock_dict["date"] = payload.date.isoformat()

    # Prevent duplicates per (stationId, fuelType, date) for sanity
    existing = await db["fuelStocks"].find_one(
        {
            "stationId": stock_dict["stationId"],
            "fuelType": stock_dict["fuelType"],
            "date": stock_dict["date"],
        }
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="FuelStock already exists for this day")

    result = await db["fuelStocks"].insert_one(stock_dict)
    created = await db["fuelStocks"].find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created


@router.get(
    "/",
    response_model=List[FuelStockResponse],
    summary="List fuel stock records (optionally filter by stationId and date)",
)
async def list_fuel_stocks(
    stationId: Optional[str] = None,
    date: Optional[date] = None,
    db=Depends(get_database),
):
    query: dict[str, object] = {}
    if stationId is not None:
        if not ObjectId.is_valid(stationId):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid stationId format")
        query["stationId"] = stationId
    if date is not None:
        query["date"] = date.isoformat()

    stocks = await db["fuelStocks"].find(query).to_list(1000)
    for s in stocks:
        s["_id"] = str(s["_id"])
    return stocks


@router.get(
    "/{id}",
    response_model=FuelStockResponse,
    summary="Get a fuel stock record by ID",
)
async def get_fuel_stock(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid FuelStock ID format")

    stock = await db["fuelStocks"].find_one({"_id": ObjectId(id)})
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FuelStock not found")

    stock["_id"] = str(stock["_id"])
    return stock


@router.put(
    "/{id}",
    response_model=FuelStockResponse,
    summary="Update a fuel stock record by ID",
)
async def update_fuel_stock(id: str, update: FuelStockUpdate, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid FuelStock ID format")

    existing = await db["fuelStocks"].find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FuelStock not found")

    update_data = update.model_dump(exclude_none=True)

    # Normalize date if present
    if "date" in update_data and isinstance(update_data["date"], date):
        update_data["date"] = update_data["date"].isoformat()

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    # If stationId is being changed, validate it
    final_station_id = update_data.get("stationId", existing["stationId"])
    try:
        final_station = await find_station(db, final_station_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not final_station:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid stationId")

    # If fuelType is being changed, validate it against the final station
    final_fuel_type = update_data.get("fuelType", existing["fuelType"])
    if not fuel_type_supported(final_station, final_fuel_type):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fuelType is not supported by this station")

    # If availableLiters is provided, ensure it is not negative (pydantic covers it, but keep extra safety)
    if "availableLiters" in update_data and update_data["availableLiters"] < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="availableLiters cannot be negative")

    await db["fuelStocks"].update_one({"_id": ObjectId(id)}, {"$set": update_data})
    updated = await db["fuelStocks"].find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return updated


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a fuel stock record by ID",
)
async def delete_fuel_stock(id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid FuelStock ID format")

    result = await db["fuelStocks"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FuelStock not found")
    return None


@router.get(
    "/station/{stationId}",
    response_model=List[FuelStockResponse],
    summary="List fuel stock records for a station",
)
async def list_by_station(stationId: str, db=Depends(get_database)):
    if not ObjectId.is_valid(stationId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid stationId format")
    stocks = await db["fuelStocks"].find({"stationId": stationId}).to_list(1000)
    for s in stocks:
        s["_id"] = str(s["_id"])
    return stocks


@router.patch(
    "/deduct",
    summary="Deduct available liters from today's FuelStock (optional transaction tracking)",
)
async def deduct_fuel_stock(payload: FuelStockDeduct, db=Depends(get_database)):
    # Validate station exists and supports this fuel type
    try:
        station = await find_station(db, payload.stationId)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not station:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid stationId")

    if not fuel_type_supported(station, payload.fuelType):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fuelType is not supported by this station")

    stock_date = payload.date.isoformat() if payload.date is not None else utc_today_date().isoformat()

    stock = await db["fuelStocks"].find_one(
        {"stationId": payload.stationId, "fuelType": payload.fuelType, "date": stock_date}
    )
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FuelStock for this station/fuelType/date not found",
        )

    if stock.get("availableLiters", 0) < payload.liters:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough fuel available")

    update_ops: dict[str, object] = {"$inc": {"availableLiters": -payload.liters}}
    if payload.transactionId:
        update_ops["$addToSet"] = {"transactions": payload.transactionId}

    await db["fuelStocks"].update_one(
        {"_id": stock["_id"]},
        update_ops,
    )

    updated = await db["fuelStocks"].find_one({"_id": stock["_id"]})
    updated["_id"] = str(updated["_id"])
    return updated

