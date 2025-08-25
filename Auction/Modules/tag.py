import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Emojis
EMOJIS = [
    "🦁", "🐯", "🐱", "🐶", "🐺", "🐻",
    "🐻‍❄️", "🐨", "🐼", "🐹", "🐭",
    "🐰", "🦊", "🦝", "🐮", "🐷"
]

# --- /tagall command ---
async def tagall(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if sender is admin
    member = await client.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        return await message.reply_text("❌ Only group admins can use this command!")

    # Tag text
    tag_text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:]) or ""

    # Inline buttons
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Send", callback_data="send_tag"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel_tag")]
    ])

    # Emoji preview
    emojiline = " ".join(random.choices(EMOJIS, k=10))
    await message.reply_text(f"{tag_text}\n\nPreview: {emojiline}", reply_markup=markup)

# --- Handle callback buttons ---
async def handle_buttons(client: Client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "cancel_tag":
        return await callback_query.edit_message_text("❌ Tagging cancelled.")

    if data == "send_tag":
        await callback_query.edit_message_text("🚀 Tagging started...")

        members = []
        async for m in client.iter_chat_members(chat_id):
            if m.user.is_bot or m.user.is_deleted:
                continue
            members.append(m.user)

        if not members:
            return await callback_query.edit_message_text("⚠️ No valid members found to tag.")

        # Tag in batches
        chunk_size = 5
        text = callback_query.message.text.split("\n\n")[0]

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
            f"✅ Tagging completed!\n👤 Number of users tagged: `{len(members)}`\n💬 Started by: [{callback_query.from_user.first_name}](tg://user?id={user_id})",
            parse_mode="markdown"
        )

# --- Register function for __main__.py ---
def register(app: Client):
    app.add_handler(app.on_message(filters.command("tagall") & filters.group)(tagall))
    app.add_handler(app.on_callback_query(filters.regex("^(send_tag|cancel_tag)$"))(handle_buttons))