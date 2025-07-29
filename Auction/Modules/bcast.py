from pyrogram import filters
from pyrogram.types import Message
from Auction import bot
from Auction.db import get_all_users, get_all_groups
from config import ADMINS
import asyncio

@bot.on_message(filters.command("bcast") & filters.user(ADMINS))
async def broadcast_handler(_, message: Message):
    if message.reply_to_message:
        content = message.reply_to_message
    else:
        text = message.text.split(None, 1)
        if len(text) < 2:
            return await message.reply("❌ ᴇxᴀᴍᴘʟᴇ:\n\n`/bcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]`")
        content = text[1]

    status = await message.reply("» sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...")
    total, pinned = 0, 0

    # Users
    async for user in get_all_users():
        try:
            if isinstance(content, Message):
                await content.copy(user["_id"])
            else:
                await bot.send_message(user["_id"], content)
            total += 1
            await asyncio.sleep(0.03)
        except:
            pass

    # Groups
    async for group in get_all_groups():
        try:
            if isinstance(content, Message):
                sent = await content.copy(group["_id"])
            else:
                sent = await bot.send_message(group["_id"], content)
            total += 1
            try:
                await sent.pin(disable_notification=True)
                pinned += 1
            except:
                pass
            await asyncio.sleep(0.03)
        except:
            pass

    await status.edit(f"» ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {total} ᴄʜᴀᴛs ᴡɪᴛʜ {pinned} ᴘɪɴs ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.")