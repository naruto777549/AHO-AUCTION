from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Auction import bot
from Auction.db import start_tag, stop_tag, is_tagging_active, get_tag_data
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
    user_id = cb.from_user.id

    data = await get_tag_data(chat_id)
    if not data:
        return await cb.answer("❌ No tag operation pending.", show_alert=True)

    if cb.data == "cancel_tag":
        await stop_tag(chat_id)
        return await cb.edit_message_text("❌ Tagging cancelled.")

    if cb.data == "send_tag":
        await cb.edit_message_text("🚀 Tagging started...")

        users = []
        async for member in bot.get_chat_members(chat_id):
            if not member.user.is_bot:
                users.append(member.user)

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

        if await is_tagging_active(chat_id):
            await stop_tag(chat_id)
            await bot.send_message(
                chat_id,
                f"✅ Process Completed!\n"
                f"👤 Number of tagged users: `{len(users)}`\n"
                f"💬 Tag operation started by: [{cb.from_user.first_name}](tg://user?id={user_id})",
                disable_web_page_preview=True
            )