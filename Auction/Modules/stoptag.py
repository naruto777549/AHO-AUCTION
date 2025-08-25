import logging
from pyrogram import Client, filters
from Auction.db import stop_tag, is_tagging_active

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- /stoptag command ---
@Client.on_message(filters.command("stoptag") & filters.group)
async def stop_tag_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if user is admin
    member = await client.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        logger.info(f"Non-admin user {user_id} tried to use /stoptag in chat {chat_id}")
        return await message.reply_text("❌ You must be an admin to use this command!")

    if await is_tagging_active(chat_id):
        await stop_tag(chat_id)
        await message.reply_text("🛑 Tagging stopped successfully.")
    else:
        await message.reply_text("⚠️ There is no ongoing tagging process.")