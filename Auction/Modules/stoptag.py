from pyrogram import filters
from pyrogram.types import Message
from Auction import bot
from Auction.db import start_tag, stop_tag, is_tagging_active, get_tag_data

@bot.on_message(filters.command("stoptag") & filters.group)
async def stop_tag(_, message: Message):
    chat_id = message.chat.id

    if chat_id in active_tags:
        active_tags.pop(chat_id)
        await message.reply("🛑 Tagging stopped.")
    else:
        await message.reply("⚠️ No ongoing tag process.")