from pyrogram import filters
from pyrogram.types import Message
from Auction import bot
from Auction.db import stop_tag, is_tagging_active
from Auction.utils import is_user_admin
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bot.on_message(filters.command("stoptag") & filters.group)
async def stop_tag_command(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if user is admin
    if not await is_user_admin(bot, chat_id, user_id):
        logger.info(f"Non-admin user {user_id} tried to use /stoptag in chat {chat_id}")
        return await message.reply("❌ You must be an admin to use this command!", quote=True)

    if await is_tagging_active(chat_id):
        await stop_tag(chat_id)
        await message.reply("🛑 Tagging stopped successfully.")
    else:
        await message.reply("⚠️ There is no ongoing tagging process.")