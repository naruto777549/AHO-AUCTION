from pyrogram import filters
from pyrogram.types import Message
from Auction import bot
from Auction.db import get_all_users, get_all_groups
import asyncio

OWNER_ID = 7576729648  # 🔁 Replace with your real owner ID

@bot.on_message(filters.command("bcast") & filters.user(OWNER_ID))
async def broadcast_handler(_, message: Message):
    if message.reply_to_message:
        content = message.reply_to_message
    else:
        text = message.text.split(None, 1)
        if len(text) < 2:
            return await message.reply("❌ Give a message or reply to one.")
        content = text[1]

    sent, failed = 0, 0

    # Users
    async for user in get_all_users():
        try:
            if isinstance(content, Message):
                await content.copy(user["_id"])
            else:
                await bot.send_message(user["_id"], content)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    # Groups
    async for group in get_all_groups():
        try:
            if isinstance(content, Message):
                await content.copy(group["_id"])
            else:
                await bot.send_message(group["_id"], content)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    await message.reply(f"✅ Broadcast Done!\n\n✅ Sent: {sent}\n❌ Failed: {failed}")