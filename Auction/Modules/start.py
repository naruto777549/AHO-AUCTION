from pyrogram import filters
from pyrogram.types import Message
from config import bot

@bot.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    await message.reply("👋 Welcome! Use /help to see commands.")