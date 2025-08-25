from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from Auction.db import save_user, save_group

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.effective_chat.type
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if chat_type == "private":
        # Private chat: save user
        await save_user(user_id)

        me = await context.bot.get_me()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{me.username}?startgroup=true")],
            [
                InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/God_X_Pawan"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Aho_Community")
            ],
            [
                InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Uzumaki_X_Naruto_6"),
                InlineKeyboardButton("ᴍᴀɪɴ ɢᴄ", url="https://t.me/+3GuE8k8XsuJhODY1")
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

    else:
        # Group chat: save group
        await save_group(chat_id)
        await update.message.reply_text(
            "✅ ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ & sᴀᴠᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.\n\n💡 ᴘʟᴇᴀsᴇ ᴜsᴇ /start ɪɴ ᴅᴍ ғᴏʀ ғᴜʟʟ ᴍᴇɴᴜ"
        )

def register(application: Application):
    application.add_handler(CommandHandler("start", start_handler))