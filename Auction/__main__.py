import logging
import asyncio
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH

# Import handlers
from Auction.Modules import start, tag, stoptag, ping, help, bcast

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create Pyrogram client
app = Client(
    "AhoTagBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# Register handlers if they have register functions
start.register(app)
tag.register(app)
stoptag.register(app)
ping.register(app)
help.register(app)
bcast.register(app)

if __name__ == "__main__":
    print("🚀 Aho Tagall Bot Started!")
    # Use run() instead of asyncio.run()
    app.run()