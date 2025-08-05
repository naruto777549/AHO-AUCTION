from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatMemberStatus
from Tagger import bot
from Tagger.db import start_tag, stop_tag, is_tagging_active, get_tag_data
import asyncio
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Emojis for tagging
EMOJIS = [
    "🍓", "🥭", "🍟", "🍕", "🥞", "🍱", "🥮", "🧁", "🍰",
    "🍡", "🍧", "🍨", "🍭", "🍬", "🍫", "🍩", "🎂", "🍮",
    "🍹", "🧋"
]

# Function to check if user is group admin
async def is_user_admin(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        status = member.status
        logger.info(f"Checking admin status for user {user_id} in chat {chat_id}: {status}")

        return status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False

# /tagall command handler
@bot.on_message(filters.command("tagall") & filters.group)
async def tagall(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if user is group admin (no bot admin check)
    if not await is_user_admin(bot, chat_id, user_id):
        logger.info(f"Non-admin user {user_id} tried to use /tagall in chat {chat_id}")
        return await message.reply("❌ Only group admins can use this command!", quote=True)

    if message.reply_to_message:
        tag_text = message.reply_to_message.text
    else:
        tag_text = " ".join(message.command[1:]) or None

    # Inline buttons
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Send", callback_data="send_tag"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_tag")
        ]
    ])

    # Emoji preview
    emojiline = " ".join(random.choices(EMOJIS, k=10))
    await message.reply(
        f"{tag_text if tag_text else ''}\n\n{emojiline}",
        reply_markup=markup,
        quote=True
    )

    # Save tag state in DB
    await start_tag(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        text=tag_text
    )

# Callback button handler
@bot.on_callback_query(filters.regex("^(send_tag|cancel_tag)$"))
async def handle_buttons(_, cb: CallbackQuery):
    chat_id = cb.message.chat.id
    user_id = cb.from_user.id

    data = await get_tag_data(chat_id)
    if not data:
        return await cb.answer("❌ No tag operation pending.", show_alert=True)

    if cb.data == "cancel_tag":
        await stop_tag(chat_id)
        return await cb.edit_message_text("❌ Tagging cancelled.")

    if cb.data == "send_tag":
        await cb.edit_message_text("🚀 Tagging started...")

        # Fetch all users
        users = []
        async for member in bot.get_chat_members(chat_id):
            if not member.user.is_bot:
                users.append(member.user)

        # Tag in chunks
        chunk_size = 5
        text = data.get("text") or ""
        for i in range(0, len(users), chunk_size):
            if not await is_tagging_active(chat_id):
                break

            chunk = users[i:i+chunk_size]
            msg = text + "\n\n"

            for u in chunk:
                emoji = random.choice(EMOJIS)
                msg += f"[{emoji}](tg://user?id={u.id}) "

            await bot.send_message(chat_id, msg.strip(), disable_web_page_preview=True)
            await asyncio.sleep(2)

        # Final status message
        if await is_tagging_active(chat_id):
            await stop_tag(chat_id)
            await bot.send_message(
                chat_id,
                f"✅ Process Completed!\n"
                f"👤 Number of tagged users: `{len(users)}`\n"
                f"💬 Tag operation started by: [{cb.from_user.first_name}](tg://user?id={user_id})",
                disable_web_page_preview=True
            )