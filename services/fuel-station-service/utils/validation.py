from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from bson import ObjectId


def object_id_or_raise(value: str, field_name: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise ValueError(f"Invalid {field_name}")
    return ObjectId(value)


def utc_today_date() -> date:
    return datetime.utcnow().date()


def fuel_type_supported(station_doc: dict[str, Any], fuel_type: str) -> bool:
    fuel_types = station_doc.get("fuelTypes", [])
    return fuel_type in fuel_types


async def find_station(db, station_id: str) -> Optional[dict[str, Any]]:
    station_oid = object_id_or_raise(station_id, "stationId")
    return await db["stations"].find_one({"_id": station_oid})

