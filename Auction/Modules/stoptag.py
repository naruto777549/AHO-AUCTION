import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from Auction.db import stop_tag, is_tagging_active
from Auction.utils import is_user_admin

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def stop_tag_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Check if user is admin
    if not await is_user_admin(context.bot, chat_id, user_id):
        logger.info(f"Non-admin user {user_id} tried to use /stoptag in chat {chat_id}")
        return await update.message.reply_text("❌ You must be an admin to use this command!")

    if await is_tagging_active(chat_id):
        await stop_tag(chat_id)
        await update.message.reply_text("🛑 Tagging stopped successfully.")
    else:
        await update.message.reply_text("⚠️ There is no ongoing tagging process.")

def register(application: Application):
    application.add_handler(CommandHandler("stoptag", stop_tag_command))