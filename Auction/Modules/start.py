from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Auction import bot  
from Auction.db import save_user, save_group

@bot.on_message(filters.command("start"))
async def start(_, message: Message):

    if message.chat.type == "private":
        await save_user(message.from_user.id)

        await message.reply_text(
            """🌀 ᴛᴀɢᴀʟʟ ʙᴏᴛ
➖➖➖➖➖➖➖➖➖➖➖➖
‣ ᴀᴜᴛᴏ-ᴛᴀɢ ᴀʟʟ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ɪɴ ᴄʜᴜɴᴋs
‣ ᴜsᴇ /tagall ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴇᴠᴇʀʏᴏɴᴇ
‣ sᴜᴘᴘᴏʀᴛs ʀᴇᴘʟʏ + ᴄᴜsᴛᴏᴍ ᴍᴇssᴀɢᴇ
‣ sᴛᴏᴘ ᴛᴀɢ ᴀɴʏᴛɪᴍᴇ ᴜsɪɴɢ /stoptag
➖➖➖➖➖➖➖➖➖➖➖➖
ᴇᴀsʏ ᴛᴏ ᴜsᴇ & ғᴜʟʟʏ ғᴜɴᴄᴛɪᴏɴᴀʟ ᴛᴀɢɢɪɴɢ ʙᴏᴛ ғᴏʀ ɢʀᴏᴜᴘs 🚀""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{bot.me.username}?startgroup=true")],
                [
                    InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/Uzumaki_X_Naruto_6"),
                    InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/Aho_Hexa_Auction")
                ]
            ]),
            disable_web_page_preview=True
        )

    else:
        await save_group(message.chat.id)
        await message.reply_text("✅ ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɢʀᴏᴜᴘ & sᴀᴠᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.")