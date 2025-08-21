import os
import importlib
import asyncio
from pyrogram import idle
from Auction import bot

# Path to the modules folder
MODULES_PATH = "Auction/Modules"


def load_modules():
    """Auto load all modules from Auction/Modules"""
    for filename in os.listdir(MODULES_PATH):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"Auction.Modules.{filename[:-3]}"
            importlib.import_module(module_name)
            print(f"✅ Loaded module: {module_name}")


async def startup_message():
    """Send startup message to owner"""
    try:
        await bot.send_message(
            7576729648,  # apna owner id yaha rakho
            "**[⚔️ REVENGERS BOT IS STARTING... ⚔️]**"
        )
    except Exception as e:
        print(f"⚠️ Failed to send startup message: {e}")


if __name__ == "__main__":
    print("[⚔️ REVENGERS BOT STARTING ⚔️]")
    load_modules()
    bot.start()
    asyncio.get_event_loop().run_until_complete(startup_message())
    idle()
    print("[❌ BOT STOPPED ❌]")