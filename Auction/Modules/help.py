from pyrogram import filters
from pyrogram.types import Message
from Auction import bot

@bot.on_message(filters.command("help"))
async def help_cmd(_, message: Message):
    await message.reply("""
**🤖 Bot Commands:**
/start - Start the bot
/help - Show this message
/tagall [msg] - Tag all users (GC only)
/stoptag - Stop ongoing tag
/bcast - Broadcast (Admins only)
    """)