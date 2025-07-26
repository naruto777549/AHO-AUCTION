import json
import telebot
from telebot import types
import threading
import time
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
from jinja2 import Template


API_TOKEN = '7980655265:AAEuy-ZPVxkOSY8BydegX0MAJRLfEiG-eOM'
admin_id = [6969086416,7406582778,6642049252,1897434080] 
xmods = [6969086416,7406582778,6642049252,1897434080] 
import telebot
bot = telebot.TeleBot(API_TOKEN)

# Function to check if user is admin
def is_admin(user_id):
    return user_id in admin_id

user_join_status = {}
user_states = {}
started_users = set()
banned_users = set()
broad_users = []
c = 0
sub_process = False

WELCOME_STICKER_ID = 'CAACAgEAAxkBAAENYoZnagebeFQjjClqjKELnFcaaBvPLwACkgADy7gIFZplGy0ksfj_NgQ'
WARNING_STICKER_ID = 'CAACAgEAAxkBAAENYoxnagn4itpNSinKqSfWqPjFYz-oagACnQADy7gIFdZeCTVtYsoMNgQ'
SOLD_STICKER_ID ='CAACAgEAAxkBAAENYpRnahIw3vamSFqCymixG_N5ZYsqdQAClAADy7gIFek9gAdhFRVrNgQ'
THINK_STICKER_ID = 'CAACAgEAAxkBAAENYpZnahU0RlgFICbPg9MhVFIYFJSkqgACmwADy7gIFfkLQu4X9LxKNgQ'
ANGRY_STICKER_ID = 'CAACAgEAAxkBAAENYphnahXJlDkmAWZ9JN_oKgbTFMSmFwACmAADy7gIFV4YOsvxViF8NgQ'
DOUBT_STICKER_ID = 'CAACAgEAAxkBAAENYp9naiCsJ12HhsCs_La-GP8gkWSvyAACnAADy7gIFSmDoxff0TD-NgQ'
SAD_STICKER_ID = 'CAACAgEAAxkBAAENYqFnaiFpobLesctRj96Dzz7cS2iLWwACmgADy7gIFTcqDPitqlYdNgQ'
OK_STICKER_ID = 'CAACAgEAAxkBAAENYp1nah-WgtzXbsGIKOaFd3srA0x3uAACmQADy7gIFdZWbyekt05INgQ'

USER_DATA_FILE = "users.json"
CURRENT_BOT_VERSION = '3.0.0'

# Load existing user data
def load_user():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save user data
def save_user(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Global variable for user data
users = load_user()

def send_welcome_message(chat_id, username, first_name, user_id): 
    bot.send_sticker(chat_id,WELCOME_STICKER_ID)
    markup = types.InlineKeyboardMarkup()
    join_auction_btn = types.InlineKeyboardButton("Join Auction", url=f"https://t.me/allinoneAuction")
    join_trade_btn = types.InlineKeyboardButton("Join Trade", url=f"https://t.me/AllinoneHexa")
    joined_btn = types.InlineKeyboardButton("Joined", callback_data="joined")


    markup.add(join_auction_btn, join_trade_btn)
    markup.add(joined_btn)

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
def handle_start(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:           
        user_id = str(message.from_user.id)
        username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
        first_name = message.from_user.first_name
        if message.chat.type == 'private':
            args = message.text.split()
            if len(args) > 1:  # If there's a parameter after /start
                param = args[1]  # Extract the parameter (e.g., "command_sort")
                
                if param == 'add':
                    sell(message)
                    return
                elif param == 'start':
                    send_welcome_message(message.chat.id,username,first_name,user_id)
                    return 
                elif param == 'help':
                    help_command(message)
                    return
                elif param == 'cancel':
                    handle_cancel(message)
                    return
                elif param == 'profile':
                    set_profile_pic(message)
                    return
                elif param == 'update':
                    update_prompt(message)
                    return
                
            send_welcome_message(message.chat.id, username, first_name, user_id)
        else:
            bot.send_sticker(message.chat.id,WARNING_STICKER_ID)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
            bot.reply_to(message, "<blockquote> 𝙿𝚕𝚎𝚊𝚜𝚎 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 𝚒𝚗 𝚊 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 𝚖𝚎𝚜𝚜𝚊𝚐𝚎.</blockquote>",parse_mode="html",reply_markup=markup,disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data == "joined")
def handle_joined(call):
    user_id = call.from_user.id
    first_name = call.from_user.full_name
    username = f'@{call.from_user.username}' if call.from_user.username else f'<a href="tg://user?id={user_id}">{first_name}</a>'
    
    try:
        auction_status = bot.get_chat_member(chat_id="-1002785272450", user_id=user_id).status
        trade_status = bot.get_chat_member(chat_id="-1002535385226", user_id=user_id).status 
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
            
    tex = """𝘛𝘏𝘈𝘕𝘒𝘚 𝘍𝘖𝘙 𝘑𝘖𝘐𝘕𝘐𝘕𝘎 𝘖𝘜𝘙 𝘎𝘙𝘖𝘜𝘗𝘚 😊

𝘕𝘖𝘞 𝘠𝘖𝘜 𝘊𝘈𝘕 𝘈𝘋𝘋 𝘠𝘖𝘜𝘙 𝘐𝘛𝘌𝘔𝘚 𝘛𝘖 𝘛𝘏𝘌 𝘈𝘜𝘊𝘛𝘐𝘖𝘕 𝘉𝘠 𝘊𝘖𝘔𝘔𝘈𝘕𝘋 /𝘈𝘋𝘋

𝘉𝘌𝘍𝘖𝘙𝘌 𝘈𝘋𝘋 𝘗𝘖𝘒𝘌 𝘐𝘕 𝘈𝘜𝘊𝘛𝘐𝘖𝘕 𝘊𝘏𝘌𝘊𝘒 𝘙𝘜𝘓𝘌𝘚 𝘓𝘈𝘛𝘌𝘙 𝘋𝘖𝘕'𝘛 𝘊𝘖𝘔𝘗𝘓𝘈𝘐𝘕 𝘛𝘖 𝘛𝘏𝘌 𝘈𝘋𝘔𝘐𝘕. 𝘍𝘖𝘙 𝘊𝘏𝘌𝘊𝘒𝘐𝘕𝘎 𝘙𝘜𝘓𝘌𝘚 𝘜𝘚𝘌 𝘊𝘖𝘔𝘔𝘈𝘕𝘋 /𝘙𝘜𝘓𝘌𝘚"""

    if has_joined_auction and has_joined_trade:
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=tex,
            parse_mode='html')

@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        global sub_process
        if message.chat.type == 'private':
            user_id = message.from_user.id
            if user_id in user_states:
                del user_states[user_id]
            sub_process = False
            bot.send_message(message.chat.id, "<blockquote>𝙰𝚕𝚕 𝙲𝚘𝚖𝚖𝚊𝚗𝚍 𝙿𝚛𝚘𝚌𝚎𝚜𝚜 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚌𝚊𝚗𝚌𝚎𝚕𝚕𝚎𝚍 ✅</blockquote>",parse_mode="html")
        else:
            bot.send_sticker(message.chat.id,WARNING_STICKER_ID)
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('cancel',url='https://t.me/Auct_he_bot?start=cancel'))
            bot.reply_to(message, "<blockquote>𝙿𝚕𝚎𝚊𝚜𝚎 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 𝚒𝚗 𝚊 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 𝚖𝚎𝚜𝚜𝚊𝚐𝚎.</blockquote>",parse_mode="html",reply_markup=markup,disable_web_page_preview=True)


# Placeholder lists, replace these with actual data
dxgays = []  # List of user IDs that are in dxgays
  # List of user IDs that are xmods
user_cache = {}

# Constants, replace with actual values
AUCTION_GROUP_LINK = 'your_auction_group_link_here'
AUCTION_GROUP_LINK = 'https://t.me/+PXgGASqusSMxZjU9'
log_channel = -1002611946558  # Replace with your log channel ID
post_channel = -1002785272450  # Replace with your post channel ID
approve_channel = -1002611946558  # Replace with your approve channel ID
reject_channel = -1002611946558  # Replace with your reject channel ID

pokemon_name = ""
items = []
msg = []

@bot.message_handler(commands=['add'])
def sell(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    
    if not has_started_bot(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('start',url='https://t.me/aho_auction_bot?start=start'))
        bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    if not is_user_updated(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('update',url='https://t.me/aho_auction_bot?start=update'))
        bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return

    if message.chat.type != 'private':
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('ADD',url='https://t.me/Aho_auction_bot?start=add'))
        bot.reply_to(message, '<blockquote><b>Use this command in my dm.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    if user_id in dxgays:
        bot.send_message(user_id, f"Ho Ho Ho\n\nIf you want to sell something in auction how about you sell your mom to xmods. "
                                 f"Although your moms are already free WHORE whose price is free for a year to use by anyone and they have such loose pussy.\n\n"
                                 f"{first_name} mom has got best whore award, {first_name} is trying to find about his real dad, when {first_name} fills any form in father section he writes xmods and 3.97 billion others.")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Yes', callback_data='yes'))
        markup.add(types.InlineKeyboardButton('No', callback_data='No'))
        if username:
            bot.send_sticker(message.chat.id,THINK_STICKER_ID)
            bot.send_message(user_id, f"𝘏𝘦𝘭𝘭𝘰 @{username}!\n\n<blockquote>𝘞𝘰𝘶𝘭𝘥 𝘠𝘰𝘶 𝘓𝘪𝘬𝘦 𝘛𝘰 𝘚𝘦𝘭𝘭 𝘚𝘰𝘮𝘦𝘵𝘩𝘪𝘯𝘨 𝘐𝘯 𝘈𝘶𝘤𝘵𝘪𝘰𝘯?</blockquote>",parse_mode="html", reply_markup=markup)
        else:
            bot.send_sticker(message.chat.id,THINK_STICKER_ID)
            bot.send_message(user_id, "<blockquote>𝘏𝘦𝘭𝘭𝘰!\n\n𝘞𝘰𝘶𝘭𝘥 𝘠𝘰𝘶 𝘓𝘪𝘬𝘦 𝘛𝘰 𝘚𝘦𝘭𝘭 𝘚𝘰𝘮𝘦𝘵𝘩𝘪𝘯𝘨 𝘐𝘯 𝘈𝘶𝘤𝘵𝘪𝘰𝘯?</blockquote>",parse_mode="html", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['team','deletet','submitt','yes', 'No','tea', 'legendary', 'ol', 'shiny', 'tms', 'submit', 'delete', 'submi', 'delet', 'approve', 'reject', 'rejtrash', 'rejinco', 'highbase', 'scammer','lls','pls','shini','tme','back'])
def callback_handler(call):
    global sub_process
    if call.data.startswith("s_"):
        handle_sell_pokemon(call)
        return
    user_id = call.from_user.id
    if call.data == 'yes':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('𝟲𝗹⚡️', callback_data='legendary'))
        markup.add(types.InlineKeyboardButton('𝟬𝗹 🌪', callback_data='ol'))
        markup.add(types.InlineKeyboardButton('𝗦𝗵𝗶𝗻𝘆 ✨', callback_data='shiny'))
        markup.add(types.InlineKeyboardButton('𝗧𝗺𝘀 💿', callback_data='tms'))
        markup.add(types.InlineKeyboardButton('𝗧𝗲𝗮𝗺𝘀 🎯', callback_data='tea'))
        bot.edit_message_text('𝘚𝘰 𝘞𝘩𝘢𝘵 𝘞𝘰𝘶𝘭𝘥 𝘠𝘰𝘶 𝘓𝘪𝘬𝘦 𝘛𝘰 𝘚𝘦𝘭𝘭?', call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == 'No':
        bot.edit_message_text('𝙾𝙺! 𝙷𝙰𝚅𝙴 𝙰 𝙶𝚁𝙴𝙰𝚃 𝙳𝙰𝚈 ✨', call.message.chat.id, call.message.message_id)
    elif call.data == 'legendary':
        if len(legpoke_name) > 19:
            sub_process = True
            bot.edit_message_text('ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ɪɴ ᴛʜɪs ᴄᴀᴛᴇɢᴏʀʏ\n --ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ʏᴏᴜʀ ɪᴛᴇᴍs ɪɴ ɴᴇxᴛ ᴀᴜᴄᴛɪᴏɴ.....', call.message.chat.id, call.message.message_id)
        else:    
            handle_legendary(call)
            sub_process = True
    elif call.data == 'ol':
        if len(nonleg_name) > 49:
            sub_process = True
            bot.edit_message_text('ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ɪɴ ᴛʜɪs ᴄᴀᴛᴇɢᴏʀʏ\n --ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ʏᴏᴜʀ ɪᴛᴇᴍs ɪɴ ɴᴇxᴛ ᴀᴜᴄᴛɪᴏɴ.....', call.message.chat.id, call.message.message_id)
        else:
            handle_non_legendary(call)
            sub_process = True
    elif call.data == 'shiny':
        if len(shineiess) > 9:
            sub_process = True
            bot.edit_message_text('ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ɪɴ ᴛʜɪs ᴄᴀᴛᴇɢᴏʀʏ\n --ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ʏᴏᴜʀ ɪᴛᴇᴍs ɪɴ ɴᴇxᴛ ᴀᴜᴄᴛɪᴏɴ.....', call.message.chat.id, call.message.message_id)
        else:
            handle_shiny(call)
            sub_process = True
    elif call.data == 'tms':
        if len(tmen) > 14:
            sub_process = True
            bot.edit_message_text('ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ɪɴ ᴛʜɪs ᴄᴀᴛᴇɢᴏʀʏ\n --ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ʏᴏᴜʀ ɪᴛᴇᴍs ɪɴ ɴᴇxᴛ ᴀᴜᴄᴛɪᴏɴ.....', call.message.chat.id, call.message.message_id)
        else:
            handle_tms(call)
            sub_process = True
    elif call.data == 'tea':
        if len(teams) > 4:
            sub_process = True
            bot.edit_message_text('ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ɪɴ ᴛʜɪs ᴄᴀᴛᴇɢᴏʀʏ\n --ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ʏᴏᴜʀ ɪᴛᴇᴍs ɪɴ ɴᴇxᴛ ᴀᴜᴄᴛɪᴏɴ.....', call.message.chat.id, call.message.message_id)
        else:
            handle_teams(call)
            sub_process = True
    elif call.data == 'submit':
        submit_item(call)
    elif call.data == 'delete':
        bot.edit_message_text("RESPONSE DELETED", call.message.chat.id, call.message.message_id)
    elif call.data == 'submitt':
        submit_teams(call)
    elif call.data == 'deletet':
        bot.edit_message_text("RESPONSE DELETED", call.message.chat.id, call.message.message_id)
    elif call.data == 'back':
        bot.edit_message_caption("𝙾𝙺! 𝙷𝙰𝚅𝙴 𝙰 𝙶𝚁𝙴𝙰𝚃 𝙳𝙰𝚈 ✨", call.message.chat.id, call.message.message_id)
    elif call.data == 'lls':
        legendary_ele(call)
    elif call.data == 'pls':
        nonleg_ele(call)
    elif call.data == 'shini':
        shiny_ele(call)
    elif call.data == 'tme':
        tm_ele(call)
    elif call.data == 'submi':
        submit_tm(call)
    elif call.data == 'delet':
        bot.edit_message_text("RESPONSE DELETED", call.message.chat.id, call.message.message_id)
    elif call.data in ['approve', 'reject', 'rejtrash', 'rejinco', 'highbase', 'scammer']:
        handle_admin_actions(call)
    elif call.data == 'team':
        team_ele(call)

def handle_legendary(call):
    bot.edit_message_text(f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ OK! ✨\n📜 Send Legendary Pokémon Details 🏆\n━━━━━━━━━━━━━━━━━━━━━━━━━━",call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, 
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🎮 𝙿𝚘𝚔𝚎𝚖𝚘𝚗 Submission 𝚂𝚝𝚊𝚛𝚝𝚎𝚍!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"🖊️ 𝙴𝚗𝚝𝚎𝚛 𝚝𝚑𝚎 𝙿𝚘𝚔𝚎𝚖𝚘𝚗 𝙽𝚊𝚖𝚎 ⬇️\n\n"
                        f"✅ 𝙼𝚊𝚔𝚎 𝚜𝚞𝚛𝚎 𝚒𝚝’𝚜 𝚝𝚑𝚎 𝚌𝚘𝚛𝚛𝚎𝚌𝚝 𝚗𝚊𝚖𝚎!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
                        )
    bot.register_next_step_handler_by_chat_id(call.from_user.id, process_pokemon_name, 'legendary')

def handle_non_legendary(call):
    bot.edit_message_text(f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ OK! ✨\n📜 Send Non-Legendary Pokémon Details 🏆\n━━━━━━━━━━━━━━━━━━━━━━━━━━",call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, 
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🎮 𝙿𝚘𝚔𝚎𝚖𝚘𝚗 Submission 𝚂𝚝𝚊𝚛𝚝𝚎𝚍!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"🖊️ 𝙴𝚗𝚝𝚎𝚛 𝚝𝚑𝚎 𝙿𝚘𝚔𝚎𝚖𝚘𝚗 𝙽𝚊𝚖𝚎 ⬇️\n\n"
                        f"✅ 𝙼𝚊𝚔𝚎 𝚜𝚞𝚛𝚎 𝚒𝚝’𝚜 𝚝𝚑𝚎 𝚌𝚘𝚛𝚛𝚎𝚌𝚝 𝚗𝚊𝚖𝚎!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
                        )
    bot.register_next_step_handler_by_chat_id(call.from_user.id, process_pokemon_name, 'non_legendary')

def handle_shiny(call):
    bot.edit_message_text(f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ OK! ✨\n?? Send Shiny Pokémon Details 🏆\n━━━━━━━━━━━━━━━━━━━━━━━━━━",call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, 
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🎮 𝙿𝚘𝚔𝚎𝚖𝚘𝚗 Submission 𝚂𝚝𝚊𝚛𝚝𝚎𝚍!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"🖊️ 𝙴𝚗𝚝𝚎𝚛 𝚝𝚑𝚎 𝙿𝚘𝚔𝚎𝚖𝚘𝚗 𝙽𝚊𝚖𝚎 ⬇️\n\n"
                        f"✅ 𝙼𝚊𝚔𝚎 𝚜𝚞𝚛𝚎 𝚒𝚝’𝚜 𝚝𝚑𝚎 𝚌𝚘𝚛𝚛𝚎𝚌𝚝 𝚗𝚊𝚖𝚎!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
                        )
    bot.register_next_step_handler_by_chat_id(call.from_user.id, process_pokemon_name, 'shiny')

def handle_tms(call):
    bot.edit_message_text(f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ OK! ✨\n📜 Send TM Details 🏆\n━━━━━━━━━━━━━━━━━━━━━━━━━━",call.message.chat.id, call.message.message_id)
    bot.send_message(
        call.message.chat.id,
            f"══════════════════════════\n"
            f"🏆 TM Submission Started!\n"
            f"══════════════════════════\n\n"
            f"<i>✮ <b>TM Name</b> \n"
            f"➥ <b>Step 1:</b> Forward the TM Details Page\n\n</i>"
            f"▭▭▭▭▭▭▭▭▭▭ (0%) 🔴\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote><i>⚠️ Only <b>Forwarded Messages</b> from @hexamonbot are accepted.\n</i></blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="html"
        )

    bot.register_next_step_handler_by_chat_id(call.from_user.id, process_tm, 'tm')
    
def handle_teams(call):
    bot.edit_message_text(f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ OK! ✨\n📜 Send Training Team Details 🏆\n━━━━━━━━━━━━━━━━━━━━━━━━━━",call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, 
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"🎮 𝚃𝚎𝚊𝚖 𝚂𝚞𝚋𝚖𝚒𝚜𝚜𝚒𝚘𝚗 𝚂𝚝𝚊𝚛𝚝𝚎𝚍!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"🖊️ 𝙴𝚗𝚝𝚎𝚛 𝚝𝚑𝚎 Training team 𝙽𝚊𝚖𝚎 ⬇️\n\n"
                        f"⚡️ <b>𝙴𝚡𝚊𝚖𝚙𝚕𝚎: Spa , Speed , Etc </b>\n\n"
                        f"✅ 𝙼𝚊𝚔𝚎 𝚜𝚞𝚛𝚎 𝚒𝚝’𝚜 𝚝𝚑𝚎 𝚌𝚘𝚛𝚛𝚎𝚌𝚝 𝚗𝚊𝚖𝚎!\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
                        parse_mode='html'
                        )
    bot.register_next_step_handler_by_chat_id(call.from_user.id, process_team)
    
def process_team(message):
    if not sub_process:
        return
    
    global pokemon_name
    pokemon_name = message.text
    bot.send_message(message.chat.id,
                    f"══════════════════════════\n"
                    f"🏆 Submission Process Started!\n"
                    f"══════════════════════════\n\n"
                    f"✮ Team : <b>{pokemon_name}</b>\n"
                    f"➥ 𝘚𝘵𝘦𝘱 1: 𝘍𝘰𝘳𝘸𝘢𝘳𝘥 𝘛eam 𝘗𝘢𝘨𝘦\n\n"
                    f"▭▭▭▭▭▭▭▭▭▭ (0%) 🔴\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"<blockquote>⚠️ 𝘖𝘯𝘭𝘺 𝘍𝘰𝘳𝘸𝘢𝘳𝘥𝘦𝘥 𝘔𝘦𝘴𝘴𝘢𝘨𝘦 𝘍𝘳𝘰𝘮 @hexamonbot 𝘈𝘳𝘦 𝘈𝘤𝘤𝘦𝘱𝘵𝘦𝘥\n<i><b>  -- only with level are accepted</b></i></blockquote>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
                    parse_mode="HTML"
            )
    bot.register_next_step_handler(message, process_team_page, pokemon_name)
    
import re

def is_valid_team_format(message):
    """
    Checks if the given message follows one of these formats:
    1. '<Number>. <Pokémon Name> - Lv. <Level>'
    2. '<Pokémon Name> - Lv. <Level>'
    """

    message_text = message.text.strip()
    lines = message_text.split("\n")

    # Regex patterns for both formats
    numbered_format = re.compile(r"^\d+\.\s.+\s-\sLv\.\s\d+$")  # '1. A ablast - Lv. 36'
    non_numbered_format = re.compile(r"^.+\s-\sLv\.\s\d+$")  # 'A ablast - Lv. 36'

    # Check if any line matches either format
    valid_lines = [line for line in lines if numbered_format.match(line) or non_numbered_format.match(line)]

    return len(valid_lines) > 0  # Return True if at least one valid line exists 

def process_team_page(message, name):
    if not sub_process:
        return
    
    if not is_valid_forwarded_message(message):
        bot.reply_to(message,"It is not sent from @hexamonbot Please start the process again")
        return 
    
    if not message.forward_date:  # ✅ Check if the message is forwarded
        bot.send_message(message.chat.id, "❌ Please forward the Team page, not upload a new one.")
        return
    
    if not is_valid_team_format(message):
        bot.reply_to(message, "Format is wrong send in correct format with its level")
        return
    
    bot.send_message(
            message.chat.id,
            f"══════════════════════════\n"
            f"🏆 🏆 Team Submission Progress\n"
            f"══════════════════════════\n\n"
            f"✮ <b>TM Name:</b> {pokemon_name}\n"
            f"➥ <b>Step 2:</b> Enter Base Price\n\n"
            f"▬▬▬▬▬▭▭▭▭▭ (50%) 🟠\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote> <b>💰𝘛𝘺𝘱𝘦 𝘛𝘩𝘦 𝘉𝘢𝘴𝘦 𝘗𝘳𝘪𝘤𝘦 𝘍𝘰𝘳 𝘛𝘩𝘦 𝘛𝘦𝘢𝘮𝘴 :\n  ─ Example: <code>1k, 5k, 10pd</code></b>\n</blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML"
        )
    
    tname = name
    bot.register_next_step_handler(message, process_team_base, message.text, tname)
    
def process_team_base(message, team, name):
    if not sub_process:
        return
    
    base = message.text
    user_id = message.chat.id
    fn = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else f'<a href="tg://user?id={user_id}">{fn}</a>'
    text = (
            f"#Teams\n"
            f"<b>User ID:</b> {user_id}\n"
            f"<b>Username:</b> {username}\n"
            f"<b>Base:</b> {base}\n"
            f"<b>Team name:</b> {name}\n\n"
            f"<b>About Team:\n</b>{team}\n\n"
        )

    user_cache[user_id] = {'text': text}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('SUBMIT', callback_data='submitt'))
    markup.add(types.InlineKeyboardButton('Delete', callback_data='deletet'))
    bot.send_message(user_id, text, reply_markup=markup,parse_mode='markdown')
    
def submit_teams(call):
    global pokemon_name
    bot.delete_message(call.message.chat.id, call.message.message_id)
    user_id = call.from_user.id
    text = user_cache[user_id]['text']
    ls = (
            f"<b>📜 Step 3: Team Submission</b>\n\n"
            f"▬▬▬▬▬▬▬▬▬▬▬▬ (100% Complete) ✅\n"
            f"<blockquote>✅ _Your TEAM has been successfully submitted for auction!_\n"
            f"⏳ <b>Approval Time:</b> Usually takes 3-4 hours.\n</blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
    bot.send_message(call.message.chat.id, text+ls , parse_mode='html',reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('AUCTION GROUP', url=AUCTION_GROUP_LINK)))
    bot.send_message(log_channel, text, parse_mode='html', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('APPROVE', callback_data=f'approve_{user_id}'),                                                                                
                                                                                      types.InlineKeyboardButton('REJECT', callback_data=f'reject_{user_id}')))
    
def process_pokemon_name(message, item_type):
    if not sub_process:
        return
    
    global pokemon_name
    pokemon_name = message.text
    bot.send_message(
            message.chat.id,
            f"══════════════════════════\n"
            f"🏆 Submission Process Started!\n"
            f"══════════════════════════\n\n"
            f"✮ 𝘗𝘰𝘬𝘦𝘮𝘰𝘯/𝘛𝘮 : <b>{pokemon_name}</b>\n"
            f"➥ 𝘚𝘵𝘦𝘱 1: 𝘍𝘰𝘳𝘸𝘢𝘳𝘥 𝘛𝘩𝘦 𝘕𝘢𝘵𝘶𝘳𝘦 𝘗𝘢𝘨𝘦\n\n"
            f"▭▭▭▭▭▭▭▭▭▭ (0%) 🔴\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote>⚠️ 𝘖𝘯𝘭𝘺 𝘍𝘰𝘳𝘸𝘢𝘳𝘥𝘦𝘥 𝘔𝘦𝘴𝘴𝘢𝘨𝘦 𝘍𝘳𝘰𝘮 @hexamonbot 𝘈𝘳𝘦 𝘈𝘤𝘤𝘦𝘱𝘵𝘦𝘥\n</blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML"
        )
    bot.register_next_step_handler(message, process_nature_pic, item_type, pokemon_name)
    
BOT_ID = 572621020  # Replace with the actual bot's ID

def is_valid_forwarded_message(message):
    """
    Checks if the forwarded message is from the required bot.
    Returns True if valid, False otherwise.
    """
    return message.forward_from and message.forward_from.id == BOT_ID

import re

def is_valid_nature_page(caption):
    """Checks if the caption contains a valid Pokémon nature description."""
    return bool(re.search(r"Nature:\s*(\w+)", caption))  # Matches 'Nature: <some_nature>'

def process_nature_pic(message, item_type, pokemon_name):
    """Processes the forwarded nature picture and validates the content."""
    
    if not sub_process:
        return
    
    if not message.forward_date:  # ✅ Check if the message is forwarded
        bot.send_message(message.chat.id, "❌ Please forward the nature page, not upload a new one.")
        return
    
    if not is_valid_forwarded_message(message):
        bot.reply_to(message, "❌ This message is not from the required bot.\nREQUIRED BOT :- @hexamonbot")
        return

    if message.photo and message.caption:
        if is_valid_nature_page(message.caption):  # ✅ Check if caption has valid nature details
            user_cache[message.chat.id] = {
                'pokemon_name': pokemon_name,
                'nature_pic': message.photo[-1].file_id
            }
            
            bot.send_message(
                    message.chat.id,
                    f"══════════════════════════\n"
                    f"🏆 Submission Progress\n"
                    f"══════════════════════════\n\n"
                    f"✮ 𝘗𝘰𝘬𝘦𝘮𝘰𝘯/𝘛𝘮 : <b>{pokemon_name}</b>\n"
                    f"➥ 𝘚𝘵𝘦𝘱 2: 𝘍𝘰𝘳𝘸𝘢𝘳𝘥 𝘐𝘝𝘴/𝘌𝘝𝘴 𝘗𝘢𝘨𝘦\n\n"
                    f"▬▬▬▭▭▭▭▭▭▭ (20%) 🟠\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"<blockquote>🔄 𝘔𝘶𝘴𝘵 𝘉𝘦 𝘛𝘩𝘦 𝘚𝘢𝘮𝘦 𝘐𝘮𝘢𝘨𝘦 𝘈𝘴 𝘛𝘩𝘦 𝘕𝘢𝘵𝘶𝘳𝘦 𝘗𝘢𝘨𝘦.\n⚠️ 𝘖𝘯𝘭𝘺 𝘍𝘰𝘳𝘸𝘢𝘳𝘥𝘦𝘥 𝘔𝘦𝘴𝘴𝘢𝘨𝘦 𝘍𝘳𝘰𝘮 @hexamonbot 𝘈𝘳𝘦 𝘈𝘤𝘤𝘦𝘱𝘵𝘦𝘥\n</blockquote>"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
                    parse_mode="HTML"
                )
