from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from Auction.db import save_user, save_group

async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start in private chat"""
    user_id = update.effective_user.id
    await save_user(user_id)
    
    me = await context.bot.get_me()
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{me.username}?startgroup=true")],
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/God_X_Pawan"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/Aho_Hexa_Auction")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Uzumaki_X_Naruto_6"),
            InlineKeyboardButton("ᴀᴜᴄᴛɪᴏɴ ɢᴄ", url="https://t.me/+3GuE8k8XsuJhODY1")
        ]
    ])
    
    await update.message.reply_photo(
        photo="https://files.catbox.moe/9worhw.jpg",
        caption="""┏━━━━━━━━━━━━━━━━━━━━━━━━━⧫
✾ Wᴇʟᴄᴏᴍᴇ ᴛᴏ AHO | Tagger
┗━━━━━━━━━━━━━━━━━━━━━━━━━⧫
┏━━━━━━━━━━━━━━━━━━━━━━━━━⧫
┠ ➻ Aᴜᴛᴏ-Tᴀɢ ᴀʟʟ Gʀᴏᴜᴘ Mᴇᴍʙᴇʀs
┃      Fᴀsᴛ & Rᴇʟɪᴀʙʟᴇ
┠ ➻ Cᴜsᴛᴏᴍ Mᴇssᴀɢᴇ + Rᴇᴘʟʏ Sᴜᴘᴘᴏʀᴛ
┃      Fᴜʟʟʏ Fᴜɴᴄᴛɪᴏɴᴀʟ
┠ ➻ Sᴛᴏᴘ ᴛᴀɢ ᴀɴʏᴛɪᴍᴇ ᴜsɪɴɢ /stoptag
┗━━━━━━━━━━━━━━━━━━━━━━━━━⧫

🚀 Pᴏᴡᴇʀғᴜʟ ᴛᴀɢɢɪɴɢ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘs!""",
        reply_markup=keyboard
    )

async def start_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start in groups"""
    chat_id = update.effective_chat.id
    await save_group(chat_id)
    
    await update.message.reply_text(
        "✅ ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ & sᴀᴠᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.\n\n💡 ᴘʟᴇᴀsᴇ ᴜsᴇ /start ɪɴ ᴅᴍ ғᴏʀ ғᴜʟʟ ᴍᴇɴᴜ"
    )

def register(application: Application):
    """Register handlers with the application"""
    # /start in private chats
    application.add_handler(CommandHandler("start", start_private, filters=None, chat_type="private"))
    
    # /start in groups
    application.add_handler(CommandHandler("start", start_group, filters=None, chat_type="group"))