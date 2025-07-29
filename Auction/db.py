import os
import json
from config import USER_DATA_FILE, ADMIN_ID
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot")

if not MONGO_URI or "null" in MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing or incorrect! Check your db.py file.")

# Connect to MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["TAG_BOT"]