from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from db import load_user, save_user, is_admin
from main import bot  # Make sure bot is defined in main and imported here

users = load_user()
sub_process = False
user_states = {}
banned_users = set()

def send_welcome_message(chat_id, username, first_name, user_id): 
    bot.send_sticker(chat_id, WELCOME_STICKER_ID)
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Join Auction", url="https://t.me/allinoneAuction"),
        InlineKeyboardButton("Join Trade", url="https://t.me/AllinoneHexa"),
    )
    markup.add(InlineKeyboardButton("Joined", callback_data="joined"))

    caption = (
        f" 𝚆𝚎𝚕𝚌𝚘𝚖𝚎, [{first_name}](tg://user?id={user_id}) 𝚃𝚘 AHO 𝙰𝚞𝚌𝚝𝚒𝚘𝚗 𝙱𝚘𝚝\n\n"
         "𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝚒𝚜 𝚞𝚜𝚎𝚍 𝚝𝚘 𝚊𝚍𝚍 𝚢𝚘𝚞𝚛 𝙿𝚘𝚔𝚎𝚖𝚘𝚗 𝚊𝚗𝚍 𝚃𝚖𝚜 𝚊𝚗𝚍 𝚂𝚑𝚒𝚗𝚢 𝚝𝚘 𝚝𝚑𝚎 𝙰𝚞𝚌𝚝𝚒𝚘𝚗\n\n"
         "𝚃𝚘 𝚓𝚘𝚒𝚗 𝚘𝚞𝚛 𝚃𝚛𝚊𝚍𝚎 𝙶𝚛𝚘𝚞𝚙 𝚊𝚗𝚍 𝙰𝚞𝚌𝚝𝚒𝚘𝚗 𝙶𝚛𝚘𝚞𝚙 𝚓𝚘𝚒𝚗 𝚋𝚢 𝙲𝚕𝚒𝚌𝚔𝚒𝚗𝚐 𝚝𝚑𝚎 𝚋𝚎𝚕𝚘𝚠 𝚃𝚠𝚘 𝙱𝚞𝚝𝚝𝚘𝚗"
    )

    bot.send_photo(
        chat_id,
        photo="https://i.postimg.cc/CLcgF4WM/IMG-20241226-182420-618.jpg",
        caption=caption,
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    user_id = str(message.from_user.id)
    if user_id in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
        return

    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    first_name = message.from_user.first_name

    if message.chat.type == 'private':
        args = message.text.split()
        if len(args) > 1:
            param = args[1]
            if param == 'add':
                from Modules.add import sell
                sell(message)
                return
            elif param == 'start':
                send_welcome_message(message.chat.id, username, first_name, user_id)
                return 
            elif param == 'help':
                from Modules.help import help_command
                help_command(message)
                return
            elif param == 'cancel':
                handle_cancel(message)
                return
            elif param == 'profile':
                from Modules.profile import set_profile_pic
                set_profile_pic(message)
                return
            elif param == 'update':
                from Modules.update import update_prompt
                update_prompt(message)
                return

        send_welcome_message(message.chat.id, username, first_name, user_id)
    else:
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton('start', url='https://t.me/Auct_he_bot?start=start'))
        bot.send_sticker(message.chat.id, WARNING_STICKER_ID)
        bot.reply_to(message, "<blockquote> 𝙿𝚕𝚎𝚊𝚜𝚎 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 𝚒𝚗 𝚊 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 𝚖𝚎𝚜𝚜𝚊𝚐𝚎.</blockquote>", parse_mode="html", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "joined")
def handle_joined(call: CallbackQuery):
    user_id = call.from_user.id
    first_name = call.from_user.full_name
    username = f'@{call.from_user.username}' if call.from_user.username else f'<a href="tg://user?id={user_id}">{first_name}</a>'

    try:
        auction_status = bot.get_chat_member(chat_id=post_channel, user_id=user_id).status
        trade_status = bot.get_chat_member(chat_id=-1002535385226, user_id=user_id).status
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
        bot.edit_message_caption(call.message.chat.id, call.message.message_id, caption=tex, parse_mode="html")

@bot.message_handler(commands=['cancel'])
def handle_cancel(message: Message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
        return

    global sub_process
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if user_id in user_states:
            del user_states[user_id]
        sub_process = False
        bot.send_message(message.chat.id, "<blockquote>𝙰𝚕𝚕 𝙲𝚘𝚖𝚖𝚊𝚗𝚍 𝙿𝚛𝚘𝚌𝚎𝚜𝚜 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚌𝚊𝚗𝚌𝚎𝚕𝚕𝚎𝚍 ✅</blockquote>", parse_mode="html")
    else:
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton('cancel', url='https://t.me/Auct_he_bot?start=cancel'))
        bot.send_sticker(message.chat.id, WARNING_STICKER_ID)
        bot.reply_to(message, "<blockquote>𝙿𝚕𝚎𝚊𝚜𝚎 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 𝚒𝚗 𝚊 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 𝚖𝚎𝚜𝚜𝚊𝚐𝚎.</blockquote>", parse_mode="html", reply_markup=markup)