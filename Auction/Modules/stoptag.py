from pyrogram import filters
from pyrogram.types import Message
from Auction import bot
from Auction.db import stop_tag, is_tagging_active

# Function to check if user is admin
async def is_user_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

@bot.on_message(filters.command("stoptag") & filters.group)
async def stop_tag_command(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if user is admin
    if not await is_user_admin(chat_id, user_id):
        return await message.reply("❌ You must be an admin to use this command!", quote=True)

    if await is_tagging_active(chat_id):
        await stop_tag(chat_id)
        await message.reply("🛑 Tagging stopped successfully.")
    else:
        await message.reply("⚠️ There is no ongoing tagging process.")