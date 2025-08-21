from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Auction import bot
from Auction.db import save_user, save_group


# ✅ Handle /start in private chat
@bot.on_message(filters.command("start") & filters.private)
async def start_private(_, message: Message):
    await save_user(message.from_user.id)
    me = await bot.get_me()

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
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{me.username}?startgroup=true")],
            [
                InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/God_X_Pawan"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/Aho_Hexa_Auction")
            ],
            [
                InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Uzumaki_X_Naruto_6"),
                InlineKeyboardButton("ᴀᴄᴛɪᴏɴ ɢᴄ", url="https://t.me/+3GuE8k8XsuJhODY1")
            ]
        ]),
        disable_web_page_preview=True
    )


# ✅ Handle /start in groups
@bot.on_message(filters.command("start") & filters.group)
async def start_group(_, message: Message):
    await save_group(message.chat.id)
    await message.reply_text(
        "✅ ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ & sᴀᴠᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.\n\n💡 ᴘʟᴇᴀsᴇ ᴜsᴇ /start ɪɴ ᴅᴍ ғᴏʀ ғᴜʟʟ ᴍᴇɴᴜ"
    )