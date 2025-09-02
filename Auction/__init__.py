# __init__.py
# Auction/__init__.py
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "TAGGER_BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)