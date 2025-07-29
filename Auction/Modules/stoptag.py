from pyrogram import filters
from pyrogram.types import Message
from Auction import bot
from Auction.db import stop_tag, is_tagging_active

@bot.on_message(filters.command("stoptag") & filters.group)
async def stop_tag_command(_, message: Message):
    chat_id = message.chat.id

    if await is_tagging_active(chat_id):
        await stop_tag(chat_id)
        await message.reply("🛑 Tagging stopped successfully.")
    else:
        await message.reply("⚠️ There is no ongoing tagging process.")