import asyncio
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Auction import app
from Auction.utils import is_user_admin   # ✅ yahan import

EMOJIS = ["🦁","🐯","🐱","🐶","🐺","🐻","🐼","🐹","🐭","🐰","🦊","🐮","🐷"]

@app.on_message(filters.command("tagall") & filters.group)
async def tagall(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # ✅ utils se admin check
    if not await is_user_admin(client, chat_id, user_id):
        return await message.reply_text("❌ Only admins can use this command!")

    tag_text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:]) or ""

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Send", callback_data="send_tag"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel_tag")]
    ])

    emojiline = " ".join(random.choices(EMOJIS, k=10))
    await message.reply_text(f"{tag_text}\n\nPreview: {emojiline}", reply_markup=markup)

@app.on_callback_query(filters.regex("^(send_tag|cancel_tag)$"))
async def handle_buttons(client, cq):
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id
    data = cq.data

    if data == "cancel_tag":
        return await cq.edit_message_text("❌ Tagging cancelled.")

    if data == "send_tag":
        await cq.edit_message_text("🚀 Tagging started...")

        members = []
        async for m in client.get_chat_members(chat_id):
            if not m.user.is_bot and not m.user.is_deleted:
                members.append(m.user)

        if not members:
            return await cq.edit_message_text("⚠️ No valid members found!")

        chunk_size = 5
        text = cq.message.text.split("\n\n")[0]

        for i in range(0, len(members), chunk_size):
            chunk = members[i:i+chunk_size]
            msg = text + "\n\n"
            for u in chunk:
                emoji = random.choice(EMOJIS)
                msg += f"[{emoji}](tg://user?id={u.id}) "
            await client.send_message(chat_id, msg, parse_mode="markdown")
            await asyncio.sleep(2)

        await client.send_message(
            chat_id,
            f"✅ Tagging completed!\n👤 Users tagged: `{len(members)}`\n💬 Started by: [{cq.from_user.first_name}](tg://user?id={user_id})",
            parse_mode="markdown"
        )