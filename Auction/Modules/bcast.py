import asyncio
from pyrogram import Client, filters
from config import ADMINS
from Auction.db import get_all_users, get_all_groups

# --- /bcast command ---
@Client.on_message(filters.command("bcast") & filters.user(ADMINS))
async def broadcast_handler(client: Client, message):
    # Determine broadcast content
    if message.reply_to_message:
        content = message.reply_to_message
    else:
        text = message.text.split(None, 1)
        if len(text) < 2:
            return await message.reply(
                "❌ ᴇxᴀᴍᴘʟᴇ:\n\n`/bcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]`",
                quote=True
            )
        content = text[1]

    status_msg = await message.reply("» sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...")
    total, pinned = 0, 0

    # ✅ Broadcast to Users
    users = await get_all_users()
    for user in users:
        try:
            if message.reply_to_message:
                await content.copy(user["_id"])
            else:
                await client.send_message(user["_id"], content)
            total += 1
            await asyncio.sleep(0.03)
        except Exception:
            continue

    # ✅ Broadcast to Groups
    groups = await get_all_groups()
    for group in groups:
        try:
            if message.reply_to_message:
                sent = await content.copy(group["_id"])
            else:
                sent = await client.send_message(group["_id"], content)
            
            total += 1

            # Try pinning message in groups
            try:
                await client.pin_chat_message(group["_id"], sent.message_id, disable_notification=True)
                pinned += 1
            except Exception:
                pass

            await asyncio.sleep(0.03)
        except Exception:
            continue

    await status_msg.edit_text(
        f"✅ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ `{total}` ᴄʜᴀᴛs\n"
        f"📌 ᴍᴇssᴀɢᴇ ᴘɪɴɴᴇᴅ ɪɴ `{pinned}` ɢʀᴏᴜᴘs."
    )