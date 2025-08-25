import asyncio
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from Auction.db import (
    start_tag,
    stop_tag,
    is_tagging_active,
    get_tag_data,
    get_all_users  # use this to fetch all users
)
from telegram import ChatMember

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emojis
EMOJIS = [
    "🦁", "🐯", "🐱", "🐶", "🐺", "🐻",
    "🐻‍❄️", "🐨", "🐼", "🐹", "🐭",
    "🐰", "🦊", "🦝", "🐮", "🐷"
]

# Check if user is admin
async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    try:
        member: ChatMember = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ("administrator", "creator")
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False

# /tagall command
async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Admin check
    if not await is_user_admin(update, context, user_id):
        return await update.message.reply_text("❌ Only group admins can use this command!", quote=True)

    # Tag text
    tag_text = update.message.reply_to_message.text if update.message.reply_to_message else " ".join(context.args) or None

    # Inline buttons
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Send", callback_data="send_tag"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel_tag")]
    ])

    # Emoji preview
    emojiline = " ".join(random.choices(EMOJIS, k=10))
    await update.message.reply_text(
        f"{tag_text if tag_text else ''}\n\n{emojiline}",
        reply_markup=markup
    )

    # Save tag state
    await start_tag(chat_id=chat_id, user_id=user_id, text=tag_text)

# Callback buttons
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    user_id = query.from_user.id

    data = await get_tag_data(chat_id)
    if not data:
        return await query.answer("❌ No tag operation pending.", show_alert=True)

    if query.data == "cancel_tag":
        await stop_tag(chat_id)
        return await query.edit_message_text("❌ Tagging cancelled.")

    if query.data == "send_tag":
        await query.edit_message_text("🚀 Tagging started...")

        # Fetch all users from DB
        all_users = await get_all_users()
        # Filter users that are in this group if you store group info, else tag all
        users = [u["_id"] for u in all_users if "groups" not in u or chat_id in u.get("groups", [])]

        if not users:
            await query.edit_message_text("⚠️ No users to tag in this group.")
            return

        chunk_size = 12
        text = data.get("text") or ""

        for i in range(0, len(users), chunk_size):
            if not await is_tagging_active(chat_id):
                break

            chunk = users[i:i+chunk_size]
            msg = text + "\n\n"
            for u_id in chunk:
                emoji = random.choice(EMOJIS)
                msg += f"[{emoji}](tg://user?id={u_id}) "

            await context.bot.send_message(chat_id, msg.strip(), parse_mode=ParseMode.MARKDOWN)
            await asyncio.sleep(2)

        if await is_tagging_active(chat_id):
            await stop_tag(chat_id)
            await context.bot.send_message(
                chat_id,
                f"✅ Process Completed!\n"
                f"👤 Number of tagged users: `{len(users)}`\n"
                f"💬 Tag operation started by: [{query.from_user.first_name}](tg://user?id={user_id})",
                parse_mode=ParseMode.MARKDOWN
            )

# Register handlers
def register(application: Application):
    application.add_handler(CommandHandler("tagall", tagall))
    application.add_handler(CallbackQueryHandler(handle_buttons, pattern="^(send_tag|cancel_tag)$"))