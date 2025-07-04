from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

from app.schemas.itinerary import ItineraryCreate

# Create
async def create_itinerary(db: AsyncIOMotorDatabase, data: ItineraryCreate) -> str:
    doc = data.dict()
    doc["createdAt"] = datetime.utcnow()
    result = await db["itinerary"].insert_one(doc)
    print("Inserted itinerary:", doc)
    return str(result.inserted_id)

# Read All
async def get_all_itineraries(db: AsyncIOMotorDatabase) -> List[dict]:
    cursor = db["itinerary"].find()
    itineraries = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id")
        itineraries.append(doc)
    return itineraries

# Read One by ID
async def get_itinerary_by_id(db: AsyncIOMotorDatabase, id: str) -> dict:
    doc = await db["itinerary"].find_one({"_id": ObjectId(id)})
    if doc:
        doc["id"] = str(doc["_id"])
        doc.pop("_id")
    return doc

# Update by ID
async def update_itinerary(db: AsyncIOMotorDatabase, id: str, data: ItineraryCreate) -> bool:
    result = await db["itinerary"].update_one(
        {"_id": ObjectId(id)},
        {"$set": data.dict()}
    )
    return result.modified_count == 1

# Delete by ID
async def delete_itinerary(db: AsyncIOMotorDatabase, id: str) -> bool:
    result = await db["itinerary"].delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1

