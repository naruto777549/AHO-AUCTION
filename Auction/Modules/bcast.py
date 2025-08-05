import asyncio
from pyrogram import filters
from pyrogram.types import Message
from Auction import bot
from config import ADMINS
from Auction.db import get_all_users, get_all_groups

@bot.on_message(filters.command("bcast") & filters.user(ADMINS))
async def broadcast_handler(_, message: Message):
    if message.reply_to_message:
        content = message.reply_to_message
    else:
        text = message.text.split(None, 1)
        if len(text) < 2:
            return await message.reply(
                "❌ ᴇxᴀᴍᴘʟᴇ:\n\n`/bcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]`"
            )
        content = text[1]

    status = await message.reply("» sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...")
    total, pinned = 0, 0

    # ✅ Broadcast to Users
    users = await get_all_users()
    for user in users:
        try:
            if isinstance(content, Message):
                await content.copy(user["_id"])
            else:
                await bot.send_message(user["_id"], content)
            total += 1
            await asyncio.sleep(0.03)
        except:
            pass

    # ✅ Broadcast to Groups
    groups = await get_all_groups()
    for group in groups:
        group_id = group["_id"]
        try:
            if isinstance(content, Message):
                sent = await content.copy(group_id)
            else:
                sent = await bot.send_message(group_id, content)
            total += 1

            # Pin message in groups
            try:
                await sent.pin(disable_notification=True)
                pinned += 1
            except:
                pass

            await asyncio.sleep(0.03)
        except:
            pass

    await status.edit(
        f"✅ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ `{total}` ᴄʜᴀᴛs\n"
        f"📌 ᴍᴇssᴀɢᴇ ᴘɪɴɴᴇᴅ ɪɴ `{pinned}` ɢʀᴏᴜᴘs."
    )