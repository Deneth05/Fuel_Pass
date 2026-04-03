from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from bson import ObjectId
from database.mongo import get_database
from models.citizen import CitizenCreate, CitizenUpdate, CitizenResponse
from datetime import datetime
from utils.auth import RoleChecker, get_password_hash

# Shared role checkers
auth_admin = RoleChecker(["admin"])
auth_citizen = RoleChecker(["citizen"])
auth_operator = RoleChecker(["station_operator"])
auth_staff = RoleChecker(["admin", "station_operator"])
auth_all = RoleChecker(["admin", "station_operator", "citizen"])

router = APIRouter()
db = get_database()
collection = db["citizens"]
user_collection = db["users"]

@router.post("/", 
             response_model=CitizenResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="Create a new citizen and user account",
             tags=["Citizens"])
async def create_citizen(citizen: CitizenCreate):
    """
    Register a new citizen in the system and create a corresponding user account.
    The NIC will be used as the system username.
    Initializes an empty list of registered vehicles.
    """
    try:
        # Check if citizen already exists
        existing_citizen = await collection.find_one({"NIC": citizen.NIC})
        if existing_citizen:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Citizen with this NIC already exists")
        
        # Check if user already exists
        existing_user = await user_collection.find_one({"username": citizen.NIC})
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username (NIC) already taken")

        citizen_dict = citizen.model_dump()
        password = citizen_dict.pop("password") # Remove password from citizen data
        
        # Create User Account
        user_record = {
            "username": citizen.NIC,
            "password": get_password_hash(password),
            "role": "citizen" # Updated role
        }
        await user_collection.insert_one(user_record)

        # Create Citizen Record
        citizen_dict["registeredVehicles"] = []
        citizen_dict["registeredAt"] = datetime.utcnow()
        
        result = await collection.insert_one(citizen_dict)
        created_citizen = await collection.find_one({"_id": result.inserted_id})
        # Convert _id to string for the response model
        created_citizen["_id"] = str(created_citizen["_id"])
        return created_citizen
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", 
            response_model=List[CitizenResponse],
            summary="List all citizens",
            tags=["Citizens"],
            dependencies=[Depends(auth_staff)])
async def list_citizens():
    """
    Retrieve a list of all registered citizens.
    Returns up to 100 records.
    """
    citizens = await collection.find().to_list(100)
    for c in citizens:
        c["_id"] = str(c["_id"])
    return citizens

@router.get("/{id}", 
            response_model=CitizenResponse,
            summary="Get citizen by ID",
            tags=["Citizens"],
            dependencies=[Depends(auth_all)])
async def get_citizen(id: str):
    """
    Retrieve details of a specific citizen by their unique database ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    citizen = await collection.find_one({"_id": ObjectId(id)})
    if citizen is None:
        raise HTTPException(status_code=404, detail=f"Citizen with id {id} not found")
    
    citizen["_id"] = str(citizen["_id"])
    return citizen

@router.put("/{id}", 
            response_model=CitizenResponse,
            summary="Update citizen details",
            tags=["Citizens"],
            dependencies=[Depends(auth_all)])
async def update_citizen(id: str, citizen_update: CitizenUpdate):
    """
    Update information for an existing citizen.
    Only provided fields will be updated.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in citizen_update.model_dump().items() if v is not None}
    
    if len(update_data) >= 1:
        update_result = await collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Citizen with id {id} not found")

    updated_citizen = await collection.find_one({"_id": ObjectId(id)})
    if updated_citizen is None:
        raise HTTPException(status_code=404, detail=f"Citizen with id {id} not found")
    
    updated_citizen["_id"] = str(updated_citizen["_id"])
    return updated_citizen

@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a citizen",
               tags=["Citizens"],
               dependencies=[Depends(auth_admin)])
async def delete_citizen(id: str):
    """
    Remove a citizen from the system by their ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Citizen with id {id} not found")
    return None
