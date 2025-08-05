import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB URI
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot"
)

if not MONGO_URI or "null" in MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing or incorrect! Check your db.py file.")

# Connect to MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["TAG_BOT"]

# Collections
tag_collection = db["active_tags"]
users_collection = db["users"]
groups_collection = db["groups"]

# ✅ Save user
async def save_user(user_id: int):
    await users_collection.update_one({"_id": user_id}, {"$set": {"_id": user_id}}, upsert=True)

# ✅ Save group
async def save_group(group_id: int):
    await groups_collection.update_one({"_id": group_id}, {"$set": {"_id": group_id}}, upsert=True)

# ✅ Get all users as list
async def get_all_users():
    return await users_collection.find().to_list(length=None)

# ✅ Get all groups as list
async def get_all_groups():
    return await groups_collection.find().to_list(length=None)

# ✅ Start tagging
async def start_tag(chat_id: int, user_id: int, text: str = None):
    await tag_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "chat_id": chat_id,
            "user_id": user_id,
            "text": text,
            "active": True
        }},
        upsert=True
    )

# ✅ Stop tagging
async def stop_tag(chat_id: int):
    await tag_collection.delete_one({"chat_id": chat_id})

# ✅ Check if active
async def is_tagging_active(chat_id: int):
    data = await tag_collection.find_one({"chat_id": chat_id})
    return bool(data and data.get("active", False))

# ✅ Get tag data
async def get_tag_data(chat_id: int):
    return await tag_collection.find_one({"chat_id": chat_id})

# ✅ Count total users
async def get_total_users():
    return await users_collection.count_documents({})

# ✅ Count total groups
async def get_total_groups():
    return await groups_collection.count_documents({})