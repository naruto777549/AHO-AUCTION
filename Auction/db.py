import os
import json
from config import USER_DATA_FILE, admin_id
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot")

if not MONGO_URI or "null" in MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing or incorrect! Check your db.py file.")

# Connect to MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["AUC_BOT"]

# Collections
users_collection = db["users"]
admins_collection = db["admins"]
pending_submissions_collection = db["pending_submissions"]
cooldowns_collection = db["cooldowns"]
submissions_collection = db["submissions"]
approved_items_collection = db["approved_items"]
bids_collection = db["bids"]
auction_status_collection = db["auction_status"]
submission_status_collection = db["submission_status"]
sold_collection = db["sold_submissions"]
super_admins_collection = db["super_admins"]
group_chats_collection = db["group_chats"]
user_join_status = {}
user_states = {}
started_users = set()
banned_users = set()
broad_users = []
c = 0
sub_process = False

# ── USER FUNCTIONS ──

async def get_user(user_id):
    return await users_collection.find_one({"user_id": user_id})

async def add_user(user_id, first_name=None, username=None):
    if not await get_user(user_id):
        await users_collection.insert_one({
            "user_id": user_id,
            "first_name": first_name,
            "username": username,
            "submissions": 0,
            "approved": 0,
            "rejected": 0,
            "banned": False,
            "verified": False,
            "sold_items": {
                "legendary": 0,
                "non_legendary": 0,
                "shiny": 0,
                "tms": 0,
                "teams": 0
            }
        })

async def add_group_chat(chat_id, title=None):
    await group_chats_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"title": title or "Unknown"}},
        upsert=True
    )

async def get_group_chats():
    chats = []
    async for chat in group_chats_collection.find({}):
        chats.append(chat["chat_id"])
    return chats

async def cancel_user_submission(user_id):
    await submissions_collection.delete_one({"user_id": user_id})
    await cooldowns_collection.delete_one({"user_id": user_id})

async def get_all_sold_items():
    users = []
    async for user in users_collection.find({"sold_items": {"$exists": True}}):
        total = sum(user["sold_items"].values())
        if total > 0:
            users.append({
                "user_id": user["user_id"],
                "username": user.get("username", "Unknown"),
                "first_name": user.get("first_name", "Unknown"),
                "sold_items": user["sold_items"],
                "total": total
            })
    return sorted(users, key=lambda x: x["total"], reverse=True)

async def increment_sold_item(user_id, item_type: str):
    await add_user(user_id)  # Ensure user exists
    valid_types = ["legendary", "non_legendary", "shiny", "tms", "teams"]
    if item_type not in valid_types:
        return
    await users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {f"sold_items.{item_type}": 1}}
    )

async def update_user_stats(user_id, status):
    await add_user(user_id)
    field_update = {
        "submitted": {"submissions": 1},
        "approved": {"approved": 1},
        "rejected": {"rejected": 1},
    }.get(status, {})
    if field_update:
        await users_collection.update_one({"user_id": user_id}, {"$inc": field_update})

# ── BAN/VERIFICATION ──

async def is_banned(user_id):
    user = await get_user(user_id)
    return user.get("banned", False) if user else False

async def set_banned(user_id, banned: bool = True):
    await add_user(user_id)
    await users_collection.update_one({"user_id": user_id}, {"$set": {"banned": banned}})

async def is_verified(user_id):
    user = await get_user(user_id)
    return user.get("verified", False) if user else False

async def set_verified(user_id):
    await users_collection.update_one({"user_id": user_id}, {"$set": {"verified": True}}, upsert=True)

async def set_pending(user_id):
    await users_collection.update_one({"user_id": user_id}, {"$set": {"pending_verification": True}}, upsert=True)

async def remove_pending(user_id):
    await users_collection.update_one({"user_id": user_id}, {"$unset": {"pending_verification": ""}})

# ── ADMIN FUNCTIONS ──

async def add_admin(user_id):
    if not await is_admin(user_id):
        await admins_collection.insert_one({"user_id": user_id})

async def remove_admin(user_id):
    await admins_collection.delete_one({"user_id": user_id})

# ── SUPER ADMIN FUNCTIONS ──

async def is_super_admin(user_id: int) -> bool:
    return await super_admins_collection.find_one({"user_id": user_id}) is not None

async def add_super_admin(user_id: int):
    if not await is_super_admin(user_id):
        await super_admins_collection.insert_one({"user_id": user_id})

async def remove_super_admin(user_id: int):
    await super_admins_collection.delete_one({"user_id": user_id})

async def get_all_super_admins():
    admins = []
    async for admin in super_admins_collection.find({}):
        admins.append(admin)
    return admins

# ── COOLDOWN FUNCTIONS ──

async def set_cooldown(user_id, timestamp):
    await cooldowns_collection.update_one({"user_id": user_id}, {"$set": {"timestamp": timestamp}}, upsert=True)

async def get_cooldown(user_id):
    cooldown = await cooldowns_collection.find_one({"user_id": user_id})
    return cooldown["timestamp"] if cooldown else None

# ── SUBMISSION FUNCTIONS ──

async def save_submission_to_db(user_id, data):
    await submissions_collection.update_one({"user_id": user_id}, {"$set": data}, upsert=True)

async def get_submission_from_db(user_id):
    return await submissions_collection.find_one({"user_id": user_id})

async def add_submission(user_id, name, base_price, auction_link):
    await submissions_collection.insert_one({
        "user_id": user_id,
        "name": name,
        "base_price": base_price,
        "auction_link": auction_link
    })

# ── BIDDING FUNCTIONS ──

async def place_bid(auction_id, user_id, bid_amount):
    await bids_collection.update_one(
        {"auction_id": auction_id},
        {"$set": {"highest_bid": bid_amount, "bidder_id": user_id}},
        upsert=True
    )

# ── GROUP & USER LIST ──

async def get_users():
    users = []
    async for user in users_collection.find():
        uid = user.get("user_id")
        if uid:
            users.append(uid)
    return users

# ── AUCTION & SUBMISSION STATUS ──

async def start_auction():
    await auction_status_collection.update_one({"status": "inactive"}, {"$set": {"status": "active"}}, upsert=True)

async def end_auction():
    await auction_status_collection.update_one({"status": "active"}, {"$set": {"status": "inactive"}}, upsert=True)

async def start_submission():
    await submission_status_collection.update_one({"status": "inactive"}, {"$set": {"status": "active"}}, upsert=True)

async def end_submission():
    await submission_status_collection.update_one({"status": "active"}, {"$set": {"status": "inactive"}}, upsert=True)

def load_user():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

def is_admin(user_id):
    return user_id in admin_id
