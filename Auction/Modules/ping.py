import time
import psutil
from pyrogram import Client, filters

# Database imports
from Auction.db import get_total_users, get_total_groups

# --- /ping command ---
async def ping_command(client: Client, message):
    start = time.time()
    sent_msg = await message.reply_text("🔍")
    end = time.time()

    ping = round((end - start) * 1000)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    total, used, free = map(lambda x: round(x / (1024 ** 3), 2), psutil.virtual_memory()[:3])

    total_users = await get_total_users()
    total_groups = await get_total_groups()

    await sent_msg.edit_text(
        f"""🏓 ᴘᴏɴɢ! ʙᴏᴛ ɪs ᴀʟɪᴠᴇ!

╭──[ 𝙎𝙔𝙎𝙏𝙀𝙈 𝙎𝙏𝘼𝙏𝙎 ]
├ 🧠 ʀᴀᴍ: {ram}% ᴜsᴇᴅ
├ 💾 ᴛᴏᴛᴀʟ ʀᴀᴍ: {total} GB
├ ⚙️ ᴄᴘᴜ: {cpu}%
├ 📡 ᴘɪɴɢ: {ping} ms
╰───────

╭──[ ᴛᴀɢᴀʟʟ ʙᴏᴛ ]
├ 👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}
├ 🏘️ ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs: {total_groups}
╰─────────────"""
    )

# --- register function for __main__.py ---
def register(app: Client):
    app.add_handler(
        app.on_message(filters.command("ping"))(ping_command)
    )