from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from Database.state import active_tags
import asyncio
import random

EMOJIS = ["👨‍🌾", "👩‍🍳", "🧑‍🚀", "👩‍🏫", "💀", "🧑‍🦽", "👩‍🦳", "👨‍🍳", "🧛", "🧙", "🐮"]

@bot.on_message(filters.command("tagall") & filters.group)
async def tagall(_, message: Message):
    if message.reply_to_message:
        tag_text = message.reply_to_message.text
    else:
        tag_text = " ".join(message.command[1:]) or None

    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ Send", callback_data="send_tag"),
             InlineKeyboardButton("❌ Cancel", callback_data="cancel_tag")]
        ]
    )

    emojiline = " ".join(random.choices(EMOJIS, k=10))
    await message.reply(
        f"{tag_text if tag_text else ''}\n\n{emojiline}",
        reply_markup=markup,
        quote=True
    )

    active_tags[message.chat.id] = {
        "text": tag_text,
        "from_id": message.from_user.id,
        "message_id": message.id,
        "start_msg": message
    }

@bot.on_callback_query(filters.regex("^(send_tag|cancel_tag)$"))
async def handle_buttons(_, cb):
    chat_id = cb.message.chat.id
    data = active_tags.get(chat_id)

    if not data:
        return await cb.answer("❌ No tag operation pending.", show_alert=True)

    if cb.data == "cancel_tag":
        active_tags.pop(chat_id, None)
        return await cb.edit_message_text("❌ Tagging cancelled.")

    if cb.data == "send_tag":
        await cb.edit_message_text("🚀 Tagging started...")

        users = []
        async for member in bot.get_chat_members(chat_id):
            if not member.user.is_bot:
                users.append(member.user.mention)

        text_chunks = [users[i:i+5] for i in range(0, len(users), 5)]
        for chunk in text_chunks:
            if chat_id not in active_tags:
                break
            msg = (data["text"] + "\n" if data["text"] else "") + "\n".join(chunk)
            await bot.send_message(chat_id, msg)
            await asyncio.sleep(2)

        if chat_id in active_tags:
            await bot.send_message(
                chat_id,
                f"✅ Process Completed!\n"
                f"👤 Number of tagged users: `{len(users)}`\n"
                f"💬 Tag operation started by: {cb.from_user.mention}"
            )
            active_tags.pop(chat_id, None)