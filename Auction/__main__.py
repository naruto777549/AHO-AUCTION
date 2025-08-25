import logging
import asyncio
from pyrogram import Client
from config import BOT_TOKEN,  API_ID, API_HASH

# Import Pyrogram handlers
from Auction.Modules import start, tag, stoptag, ping, help, bcast

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create Pyrogram client using config values
app = Client(
    "AhoTagBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

async def main():
    # Start the client
    await app.start()
    print("🚀 Aho Tagall Bot Started!")

    # Keep the bot running
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Register handlers if your modules have register functions
    # start.register(app)
    # tag.register(app)
    # stoptag.register(app)
    # ping.register(app)
    # help.register(app)
    # bcast.register(app)

    # Run bot
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Bot stopped.")