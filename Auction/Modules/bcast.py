from pyrogram import filters
from pyrogram.types import Message
from config import bot

@bot.on_message(filters.command("bcast") & filters.private)
async def broadcast(_, message: Message):
    if message.from_user.id not in [OWNER_ID]:  # Replace OWNER_ID
        return await message.reply("Only owner can broadcast.")

    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")

    count = 0
    async for dialog in bot.get_dialogs():
        try:
            await bot.send_message(dialog.chat.id, message.reply_to_message.text)
            count += 1
        except:
            continue
    await message.reply(f"✅ Broadcast sent to `{count}` chats.")