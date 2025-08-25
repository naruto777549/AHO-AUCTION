import asyncio
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emojis
EMOJIS = [
    "🦁", "🐯", "🐱", "🐶", "🐺", "🐻",
    "🐻‍❄️", "🐨", "🐼", "🐹", "🐭",
    "🐰", "🦊", "🦝", "🐮", "🐷"
]

# --- Check if user is admin ---
async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    try:
        member: ChatMember = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ("administrator", "creator")
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False

# --- /tagall command ---
async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Admin check
    if not await is_user_admin(update, context, user_id):
        return await update.message.reply_text("❌ Only group admins can use this command!", quote=True)

    # Tag text
    tag_text = update.message.reply_to_message.text if update.message.reply_to_message else " ".join(context.args) or ""

    # Inline buttons (optional)
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Send", callback_data="send_tag"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel_tag")]
    ])

    # Emoji preview
    emojiline = " ".join(random.choices(EMOJIS, k=10))
    await update.message.reply_text(f"{tag_text}\n\nPreview: {emojiline}", reply_markup=markup)

# --- Handle send_tag button ---
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    if query.data == "cancel_tag":
        return await query.edit_message_text("❌ Tagging cancelled.")

    if query.data == "send_tag":
        await query.edit_message_text("🚀 Tagging started...")

        # Fetch all members in the chat dynamically
        members = []
        try:
            async for m in context.bot.get_chat_members(chat_id):
                if m.user.is_bot or m.user.is_deleted:
                    continue
                members.append(m.user)
        except Exception as e:
            return await query.edit_message_text(f"⚠️ Failed to fetch members: {e}")

        if not members:
            return await query.edit_message_text("⚠️ No valid members found to tag.")

        # Tag in batches
        chunk_size = 5
        text = query.message.text.split("\n\n")[0]  # Use original tag text
        for i in range(0, len(members), chunk_size):
            chunk = members[i:i+chunk_size]
            msg = text + "\n\n"
            for u in chunk:
                emoji = random.choice(EMOJIS)
                msg += f"[{emoji}](tg://user?id={u.id}) "
            try:
                await context.bot.send_message(chat_id, msg.strip(), parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                logger.warning(f"Failed to send chunk: {e}")
            await asyncio.sleep(2)

        await context.bot.send_message(
            chat_id,
            f"✅ Tagging completed!\n👤 Number of users tagged: `{len(members)}`\n💬 Started by: [{query.from_user.first_name}](tg://user?id={user_id})",
            parse_mode=ParseMode.MARKDOWN
        )

# --- Register handlers ---
def register(application: Application):
    application.add_handler(CommandHandler("tagall", tagall))
    application.add_handler(CallbackQueryHandler(handle_buttons, pattern="^(send_tag|cancel_tag)$"))