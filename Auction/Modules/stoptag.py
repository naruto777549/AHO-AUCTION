import logging
from pyrogram import filters
from Auction import app
from Auction.db import stop_tag, is_tagging_active

logger = logging.getLogger(__name__)

@app.on_message(filters.command("stoptag") & filters.group)
async def stop_tag_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    member = await client.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        logger.info(f"Non-admin {user_id} tried /stoptag in {chat_id}")
        return await message.reply_text("❌ Only admins can stop tagging!")

    if await is_tagging_active(chat_id):
        await stop_tag(chat_id)
        await message.reply_text("🛑 Tagging stopped successfully.")
    else:
        await message.reply_text("⚠️ No ongoing tagging process.")