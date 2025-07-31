from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus  # Import enum for status
from Auction import bot
from Auction.db import stop_tag, is_tagging_active
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to check if user is admin
async def is_user_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        logger.info(f"Checking admin status for user {user_id} in chat {chat_id}: Status = {member.status}")
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except Exception as e:
        logger.error(f"Error checking admin status for user {user_id} in chat {chat_id}: {str(e)}")
        return False

@bot.on_message(filters.command("stoptag") & filters.group)
async def stop_tag_command(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if user is admin
    if not await is_user_admin(chat_id, user_id):
        logger.info(f"Non-admin user {user_id} tried to use /stoptag in chat {chat_id}")
        return await message.reply("❌ You must be an admin to use this command!", quote=True)

    if await is_tagging_active(chat_id):
        await stop_tag(chat_id)
        await message.reply("🛑 Tagging stopped successfully.")
    else:
        await message.reply("⚠️ There is no ongoing tagging process.")