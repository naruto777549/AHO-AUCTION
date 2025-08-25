from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Auction.db import save_user, save_group

# --- /start command ---
async def start_handler(client: Client, message):
    chat_type = message.chat.type
    user_id = message.from_user.id
    chat_id = message.chat.id

    if chat_type == "private":
        # Save user
        await save_user(user_id)

        me = await client.get_me()
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

        await message.reply_photo(
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
        # Save group
        await save_group(chat_id)
        await message.reply_text(
            "✅ ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ & sᴀᴠᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.\n\n💡 ᴘʟᴇᴀsᴇ ᴜsᴇ /start ɪɴ ᴅᴍ ғᴏʀ ғᴜʟʟ ᴍᴇɴᴜ"
        )

# --- register function for __main__.py ---
def register(app: Client):
    app.add_handler(app.on_message(filters.command("start"))(start_handler))