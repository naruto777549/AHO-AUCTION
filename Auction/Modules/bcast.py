import asyncio
from pyrogram import filters
from config import ADMINS
from Auction import app
from Auction.db import get_all_users, get_all_groups

@app.on_message(filters.command("bcast") & filters.user(ADMINS))
async def broadcast_handler(client, message):
    if message.reply_to_message:
        content = message.reply_to_message
    else:
        text = message.text.split(None, 1)
        if len(text) < 2:
            return await message.reply("❌ Example:\n/bcast [message or reply]")
        content = text[1]

    status = await message.reply("» Broadcasting...")
    total, pinned = 0, 0

    for user in await get_all_users():
        try:
            if message.reply_to_message:
                await content.copy(user["_id"])
            else:
                await client.send_message(user["_id"], content)
            total += 1
            await asyncio.sleep(0.03)
        except:
            continue

    for group in await get_all_groups():
        try:
            if message.reply_to_message:
                sent = await content.copy(group["_id"])
            else:
                sent = await client.send_message(group["_id"], content)
            total += 1
            try:
                await client.pin_chat_message(group["_id"], sent.id, disable_notification=True)
                pinned += 1
            except:
                pass
            await asyncio.sleep(0.03)
        except:
            continue

    await status.edit_text(f"✅ Broadcasted to `{total}` chats\n📌 Pinned in `{pinned}` groups.")