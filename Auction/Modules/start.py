from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from Auction.db import load_user, save_user, is_admin
from Auction import bot  # Make sure bot is defined in main and imported here

users = load_user()
sub_process = False
user_states = {}
banned_users = set()

def send_welcome_message(chat_id, username, first_name, user_id): 
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join Auction", url=AUCTION_GROUP_LINK),
         InlineKeyboardButton("Join Trade", url="https://t.me/AllinoneHexa")],
        [InlineKeyboardButton("Joined", callback_data="joined")]
    ])

    caption = (
        f"𝚆𝚎𝚕𝚌𝚘𝚖𝚎, [{first_name}](tg://user?id={user_id}) 𝚃𝚘 AHO 𝙰𝚞𝚌𝚝𝚒𝚘𝚗 𝙱𝚘𝚝\n\n"
        "𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝚒𝚜 𝚞𝚜𝚎𝚍 𝚝𝚘 𝚊𝚍𝚍 𝚢𝚘𝚞𝚛 𝙿𝚘𝚔𝚎𝚖𝚘𝚗 𝚊𝚗𝚍 𝚃𝚖𝚜 𝚊𝚗𝚍 𝚂𝚑𝚒𝚗𝚢 𝚝𝚘 𝚝𝚑𝚎 𝙰𝚞𝚌𝚝𝚒𝚘𝚗\n\n"
        "𝚃𝚘 𝚓𝚘𝚒𝚗 𝚘𝚞𝚛 𝚃𝚛𝚊𝚍𝚎 𝙶𝚛𝚘𝚞𝚙 𝚊𝚗𝚍 𝙰𝚞𝚌𝚝𝚒𝚘𝚗 𝙶𝚛𝚘𝚞𝚙 𝚓𝚘𝚒𝚗 𝚋𝚢 𝙲𝚕𝚒𝚌𝚔𝚒𝚗𝚐 𝚝𝚑𝚎 𝚋𝚎𝚕𝚘𝚠 𝚃𝚠𝚘 𝙱𝚞𝚝𝚝𝚘𝚗"
    )

    bot.send_sticker(chat_id, WELCOME_STICKER_ID)
    bot.send_photo(
        chat_id,
        photo="https://i.postimg.cc/CLcgF4WM/IMG-20241226-182420-618.jpg",
        caption=caption,
        reply_markup=markup,
        parse_mode="markdown"
    )

@bot.on_message(filters.command("start") & filters.private)
async def handle_start(client, message: Message):
    user_id = str(message.from_user.id)

    if user_id in banned_users:
        await message.reply("You are banned by an administrator.")
        return

    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    first_name = message.from_user.first_name

    args = message.text.split()
    if len(args) > 1:
        param = args[1].lower()
        if param == 'add':
            from Auction.Modules.add import sell
            await sell(client, message)
            return
        elif param == 'start':
            send_welcome_message(message.chat.id, username, first_name, user_id)
            return
        elif param == 'help':
            from Auction.Modules.help import help_command
            await help_command(client, message)
            return
        elif param == 'cancel':
            await handle_cancel(client, message)
            return
        elif param == 'profile':
            from Auction.Modules.profile import set_profile_pic
            await set_profile_pic(client, message)
            return
        elif param == 'update':
            from Auction.Modules.update import update_prompt
            await update_prompt(client, message)
            return

    send_welcome_message(message.chat.id, username, first_name, user_id)

@bot.on_callback_query(filters.regex("joined"))
async def handle_joined(client, call: CallbackQuery):
    user_id = call.from_user.id
    first_name = call.from_user.first_name
    username = f'@{call.from_user.username}' if call.from_user.username else f'<a href="tg://user?id={user_id}">{first_name}</a>'

    try:
        auction_status = (await bot.get_chat_member(chat_id=POST_CHANNEL, user_id=user_id)).status
        trade_status = (await bot.get_chat_member(chat_id=-1002535385226, user_id=user_id)).status
        has_joined_auction = auction_status in ['member', 'administrator', 'creator']
        has_joined_trade = trade_status in ['member', 'administrator', 'creator']
    except:
        has_joined_auction = True
        has_joined_trade = True

    if str(user_id) not in users:
        users[str(user_id)] = {
            "name": first_name,
            "username": username,
            "version": CURRENT_BOT_VERSION
        }
        save_user(users)

    if has_joined_auction and has_joined_trade:
        tex = """𝘛𝘏𝘈𝘕𝘒𝘚 𝘍𝘖𝘙 𝘑𝘖𝘐𝘕𝘐𝘕𝘎 𝘖𝘜𝘙 𝘎𝘙𝘖𝘜𝘗𝘚 😊

𝘕𝘖𝘞 𝘠𝘖𝘜 𝘊𝘈𝘕 𝘈𝘋𝘋 𝘠𝘖𝘜𝘙 𝘐𝘛𝘌𝘔𝘚 𝘛𝘖 𝘛𝘏𝘌 𝘈𝘜𝘊𝘛𝘐𝘖𝘕 𝘉𝘠 𝘊𝘖𝘔𝘔𝘈𝘕𝘋 /𝘈𝘋𝘋

𝘉𝘌𝘍𝘖𝘙𝘌 𝘈𝘋𝘋 𝘗𝘖𝘒𝘌 𝘐𝘕 𝘈𝘜𝘊𝘛𝘐𝘖𝘕 𝘊𝘏𝘌𝘊𝘒 𝘙𝘜𝘓𝘌𝘚 𝘓𝘈𝘛𝘌𝘙 𝘋𝘖𝘕'𝘛 𝘊𝘖𝘔𝘗𝘓𝘈𝘐𝘕 𝘛𝘖 𝘛𝘏𝘌 𝘈𝘋𝘔𝘐𝘕. 𝘍𝘖𝘙 𝘊𝘏𝘌𝘊𝘒𝘐𝘕𝘎 𝘙𝘜𝘓𝘌𝘚 𝘜𝘚𝘌 𝘊𝘖𝘔𝘔𝘈𝘕𝘋 /𝘙𝘜𝘓𝘌𝘚"""
        await call.message.edit_caption(caption=tex, parse_mode="html")

@bot.on_message(filters.command("cancel") & filters.private)
async def handle_cancel(client, message: Message):
    if str(message.from_user.id) in banned_users:
        await message.reply("You are banned by an administrator.")
        return

    global sub_process
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    sub_process = False
    await message.reply("<blockquote>𝙰𝚕𝚕 𝙲𝚘𝚖𝚖𝚊𝚗𝚍 𝙿𝚛𝚘𝚌𝚎𝚜𝚜 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚌𝚊𝚗𝚌𝚎𝚕𝚕𝚎𝚍 ✅</blockquote>", parse_mode="html")