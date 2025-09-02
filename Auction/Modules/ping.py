import time
import psutil
from pyrogram import filters
from Auction import app
from Auction.db import get_total_users, get_total_groups

@app.on_message(filters.command("ping"))
async def ping_command(client, message):
    start = time.time()
    msg = await message.reply_text("🔍")
    end = time.time()

    ping = round((end - start) * 1000)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    total, used, free = map(lambda x: round(x / (1024**3), 2), psutil.virtual_memory()[:3])

    users = await get_total_users()
    groups = await get_total_groups()

    await msg.edit_text(
f"""🏓 Pong! Bot is alive.

🧠 RAM: {ram}% used  
💾 Total RAM: {total} GB  
⚙️ CPU: {cpu}%  
📡 Ping: {ping} ms  

👥 Users: {users}  
🏘️ Groups: {groups}"""
    )