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

bot.register_next_step_handler(message, process_evs_pic, item_type, pokemon_name, message.caption)
        else:
            bot.send_message(message.chat.id, "❌ This doesn't seem like a valid nature page.\nPlease forward the Pokémon's nature screenshot.")
    else:
        bot.send_message(message.chat.id, "❌ An error occurred.\nPlease restart the process and ensure you forward the correct nature page.")

import re

def is_valid_evs_page(caption):
    """Checks if the caption contains a valid Pokémon IVs/EVs table."""
    ivs_evs_pattern = (
        r"Points\s+IV\s+\|\s+EV\n"
        r"[-–—]+\n"
        r"(?:.*?\d+\s+\|\s+\d+\n){6}"  # Matches 6 lines of IVs and EVs
        r"[-–—]+\n"
        r"Total\s+\d+\s+\|\s+\d+"
    )
    return bool(re.search(ivs_evs_pattern, caption, re.DOTALL))

def process_evs_pic(message, item_type, pokemon_name, nature):
    """Processes the forwarded EVs picture and validates its content."""
    
    if not sub_process:
        return
    
    # ✅ Ensure the message is forwarded
    if not hasattr(message, "forward_date") or not message.forward_date:
        bot.send_message(message.chat.id, "❌ Please forward the IVs/EVs page, do not upload a new image.")
        return
    
    if not is_valid_forwarded_message(message):
        bot.reply_to(message, "❌ This message is not from the required bot.\nREQUIRED BOT :- @hexamonbot")
        return

    # ✅ Ensure the message contains a photo
    if not hasattr(message, "photo") or not message.photo:
        bot.send_message(message.chat.id, "❌ No image detected. Please forward the Pokémon's IVs/EVs screenshot.")
        return

    # ✅ Ensure the message contains a caption
    if not message.caption:
        bot.send_message(message.chat.id, "❌ Caption missing. Please forward the Pokémon's IVs/EVs screenshot with the correct format.")
        return

    # ✅ Validate the IVs/EVs format
    if not is_valid_evs_page(message.caption):
        bot.send_message(message.chat.id, "❌ This doesn't seem like a valid IVs/EVs page.\nPlease forward the correct IVs/EVs screenshot.")
        return

    # ✅ Ensure it's the SAME image as the nature page
    if user_cache.get(message.chat.id, {}).get('nature_pic') != message.photo[-1].file_id:
        bot.send_message(message.chat.id, "❌ This image does not match the nature page. Please forward the correct IVs/EVs page.")
        return

    # ✅ Store the IVs/EVs image
    user_cache[message.chat.id]['evs_pic'] = message.photo[-1].file_id

    bot.send_message(
            message.chat.id,
            f"══════════════════════════\n"
            f"🏆 Submission Progress\n"
            f"══════════════════════════\n\n"
            f"✮ 𝘗𝘰𝘬𝘦𝘮𝘰𝘯/𝘛𝘮 : <b>{pokemon_name}</b>\n"
            f"➥ 𝘚𝘵𝘦𝘱 3: 𝘍𝘰𝘳𝘸𝘢𝘳𝘥 𝘛𝘩𝘦 𝘔𝘰𝘷𝘦𝘴𝘦𝘵 𝘗𝘢𝘨𝘦\n\n"
            f"▬▬▬▬▬▭▭▭▭▭ (40%) 🟡\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote>🔄 𝘔𝘶𝘴𝘵 𝘉𝘦 𝘛𝘩𝘦 𝘚𝘢𝘮𝘦 𝘐𝘮𝘢𝘨𝘦 𝘈𝘴 𝘛𝘩𝘦 𝘕𝘢𝘵𝘶𝘳𝘦 𝘗𝘢𝘨𝘦.\n⚠️ 𝘖𝘯𝘭𝘺 𝘍𝘰𝘳𝘸𝘢𝘳𝘥𝘦𝘥 𝘔𝘦𝘴𝘴𝘢𝘨𝘦 𝘍𝘳𝘰𝘮 @hexamonbot 𝘈𝘳𝘦 𝘈𝘤𝘤𝘦𝘱𝘵𝘦𝘥.\n</blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML"
        )


    bot.register_next_step_handler(message, process_moveset_pic, item_type, pokemon_name, nature, message.caption)

import re

def is_valid_moveset_page(caption):
    """Checks if the caption contains a valid Pokémon moveset format."""
    moveset_pattern = r"Power:\s*\d+,\s*Accuracy:\s*\d+\s*\(.+?\)"  # Matches "Power: 55, Accuracy: 100 (Physical)")
    return bool(re.search(moveset_pattern, caption, re.DOTALL))

def process_moveset_pic(message, item_type, pokemon_name, nature, evs):
    """Processes the forwarded Moveset picture and validates its content."""
    
    if not sub_process:
        return
    
    # ✅ Ensure the message is forwarded
    if not hasattr(message, "forward_date") or not message.forward_date:
        bot.send_message(message.chat.id, "❌ Please forward the Moveset page, do not upload a new image.")
        return
    
    if not is_valid_forwarded_message(message):
        bot.reply_to(message, "❌ This message is not from the required bot.\nREQUIRED BOT :- @hexamonbot")
        return

    # ✅ Ensure the message contains a photo
    if not hasattr(message, "photo") or not message.photo:
        bot.send_message(message.chat.id, "❌ No image detected. Please forward the Pokémon's Moveset screenshot.")
        return

    # ✅ Ensure the message contains a caption
    if not message.caption:
        bot.send_message(message.chat.id, "❌ Caption missing. Please forward the Pokémon's Moveset screenshot with the correct format.")
        return

    # ✅ Validate the Moveset format
    if not is_valid_moveset_page(message.caption):
        bot.send_message(message.chat.id, "❌ This doesn't seem like a valid Moveset page.\nPlease forward the correct Moveset screenshot.")
        return

    # ✅ Ensure it's the SAME image as the nature page
    if user_cache.get(message.chat.id, {}).get('nature_pic') != message.photo[-1].file_id:
        bot.send_message(message.chat.id, "❌ This image does not match the nature page. Please forward the correct Moveset page.")
        return

    # ✅ Store the Moveset image
    user_cache[message.chat.id]['moveset_pic'] = message.photo[-1].file_id

    bot.send_message(
            message.chat.id,
            f"══════════════════════════\n"
            f"🏆 Submission Progress\n"
            f"══════════════════════════\n\n"
            f"✮ 𝘗𝘰𝘬𝘦𝘮𝘰𝘯/𝘛𝘮 : <b>{pokemon_name}</b>\n"
            f"➥ 𝘚𝘵𝘦𝘱 4: 𝘐𝘴 𝘈𝘯𝘺 𝘚𝘵𝘢𝘵 𝘉𝘰𝘰𝘴𝘵𝘦𝘥?\n\n"
            f"▬▬▬▬▬▬▬▭▭▭▭ (60%) 🟢\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote><b>📢 𝘛𝘺𝘱𝘦 𝘵𝘩𝘦 𝘣𝘰𝘰𝘴𝘵𝘦𝘥 𝘴𝘵𝘢𝘵 𝘰𝘳 𝘳𝘦𝘱𝘭𝘺 '𝘕𝘰'.</b>\n</blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML"
        )


    bot.register_next_step_handler(message, process_boosted_stat, item_type, pokemon_name, nature, evs, message.caption)

def process_boosted_stat(message, item_type, pokemon_name, nature, evs, moveset):
    if not sub_process:
        return
    
    boosted = message.text
    bot.send_message(
            message.chat.id,
            f"══════════════════════════\n"
            f"🏆 Submission Progress\n"
            f"══════════════════════════\n\n"
            f"✮ 𝘗𝘰𝘬𝘦𝘮𝘰𝘯/𝘛𝘮 : <b>{pokemon_name}</b>\n"
            f"➥ 𝘚𝘵𝘦𝘱 5: 𝘌𝘯𝘵𝘦𝘳 𝘉𝘢𝘴𝘦 𝘗𝘳𝘪𝘤𝘦\n\n"
            f"▬▬▬▬▬▬▬▬▬▭▭ (80%) 🔵\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote>💰 𝘛𝘺𝘱𝘦 𝘵𝘩𝘦 𝘣𝘢𝘴𝘦 𝘱𝘳𝘪𝘤𝘦 𝘧𝘰𝘳 𝘵𝘩𝘦 𝘗𝘰𝘬𝘦𝘮𝘰𝘯:\n<b>   ─ Example: <code>1k, 2k, 500pd</code></b>\n</blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML"
        )


    bot.register_next_step_handler(message, process_base, item_type, pokemon_name, nature, evs, moveset, boosted)

def process_base(message, item_type, pokemon_name, nature, evs, moveset, boosted):
    if not sub_process:
        return
    
    base = message.text
    user_id = message.chat.id
    fn = message.from_user.full_name
    un = message.from_user.username if message.from_user.username else f'<a href="tg://user?id={user_id}">{fn}</a>'
    text = ( f"#{item_type.capitalize()}\n"
    f"<b>User id</b> - {user_id}\n"
    f"<b>Username</b> : @{un}\n"
    f"<b>Pokemon Name:</b> {pokemon_name}\n"
    f"<b>\nAbout Pokemon:-</b> \n{nature}\n\n"
    f"<b>Evs and Ivs:</b>-\n<code>{evs}</code>\n\n"
    f"<b>Moveset:-</b> \n{moveset}\n\n"
    f"<b>Boosted</b> - {boosted}\n"
    f"<b>\nBase</b> - {base}" )
    user_cache[user_id]['text'] = text
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('SUBMIT', callback_data='submit'))
    markup.add(types.InlineKeyboardButton('Delete', callback_data='delete'))
    bot.send_photo(user_id, user_cache[user_id]['nature_pic'], caption=text, reply_markup=markup, parse_mode='html')

import re

def is_valid_tm_format(message_text):
    """Checks if the message follows the correct TM format."""
    lines = message_text.split("\n")
    return len(lines) > 1  # Ensure there is at least one line for the TM name and another for details

def process_tm(message, item_type):
    """Processes forwarded TM messages and validates the format."""
    
    if not sub_process:
        return
    
    # ✅ Ensure the message is forwarded
    if not hasattr(message, "forward_date") or not message.forward_date:
        bot.send_message(message.chat.id, "❌ Please forward the TM details, do not type manually.")
        return
    
    if not is_valid_forwarded_message(message):
        bot.reply_to(message, "❌ This message is not from the required bot.\nREQUIRED BOT :- @hexamonbot")
        return

    # ✅ Ensure the message contains text
    if not message.text:
        bot.send_message(message.chat.id, "❌ No text detected. Please forward the TM details correctly.")
        return

    # ✅ Validate the TM format
    if not is_valid_tm_format(message.text):
        bot.send_message(message.chat.id, "❌ This doesn't seem like a valid TM format.\nPlease forward the correct TM details.")
        return

    # ✅ Extract the TM name (first line of the forwarded message)
    global pokemon_name
    lines = message.text.split("\n")
    pokemon_name = lines[0]  # First line is considered the TM name

    bot.send_message(
            message.chat.id,
            f"══════════════════════════\n"
            f"🏆 TM Submission Progress\n"
            f"══════════════════════════\n\n"
            f"<i>✮ <b>TM Name:</b> {pokemon_name}\n"
            f"➥ <b>Step 2:</b> Enter Base Price\n\n</i>"
            f"▬▬▬▬▬▭▭▭▭▭ (50%) 🟠\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote>💰 <i>Enter the base price for the TM:</i>\n<b>   ─ Example: <code>1k, 5k, 10pd</code>\n</b></blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML"
        )

    bot.register_next_step_handler(message, process_tm_base, message.text)

def process_tm_base(message, name):
    if not sub_process:
        return
    
    base = message.text
    user_id = message.chat.id
    fn = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else f'<a href="tg://user?id={user_id}">{fn}</a>'
    text = (
            f"#TMS\n"
            f"<b>User ID:</b> {user_id}\n"
            f"<b>Username:</b> {username}\n\n"
            f"<b>About TM:</b>\n{name}\n\n"
            f"<b>Base:</b> {base}\n\n"
        )

    user_cache[user_id] = {'text': text}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('SUBMIT', callback_data='submi'))
    markup.add(types.InlineKeyboardButton('Delete', callback_data='delet'))
    bot.send_message(user_id, text, reply_markup=markup,parse_mode='html')


def submit_item(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    user_id = call.from_user.id
    text = user_cache[user_id]['text']
    photo = user_cache[user_id]['nature_pic']
    bl = (
        f"\n\n══════════════════════════\n"
        f"🏆 Submission complete !\n"
        f"══════════════════════════\n\n"
        f"✮ 𝘗𝘰𝘬𝘦𝘮𝘰𝘯/𝘛𝘮 : <b>{pokemon_name}</b>\n"
        f"➥ 𝘈𝘶𝘤𝘵𝘪𝘰𝘯 𝘐𝘴 𝘙𝘦𝘢𝘥𝘺!\n\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬ (100%) ✅\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<blockquote>✅ 𝗬𝗼𝘂𝗿 𝗣𝗼𝗸𝗲𝗺𝗼𝗻 𝗜𝘀 𝗦𝗲𝗻𝘁 𝗙𝗼𝗿 𝗦𝘂𝗯𝗺𝗶𝘀𝘀𝗶𝗼𝗻!\n📢 𝗔𝗳𝘁𝗲𝗿 𝗔𝗰𝗰𝗲𝗽𝘁 𝗢𝗿 𝗥𝗲𝗷𝗲𝗰𝘁 𝗬𝗼𝘂 𝗪𝗶𝗹𝗹 𝗕𝗲 𝗡𝗼𝘁𝗶𝗳𝗶𝗲𝗱\n</blockquote>"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    bot.send_message(call.message.chat.id, text + bl,parse_mode='html', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('AUCTION GROUP', url=AUCTION_GROUP_LINK)))
    bot.send_photo(log_channel, photo, caption=text, parse_mode='html', reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('APPROVE', callback_data=f'approve_{user_id}'),
        types.InlineKeyboardButton('REJECT', callback_data=f'reject_{user_id}')))


def submit_tm(call):
    global pokemon_name
    bot.delete_message(call.message.chat.id, call.message.message_id)
    user_id = call.from_user.id
    text = user_cache[user_id]['text']
    ls = (
            f"══════════════════════════\n<b>🏆 Submission complete !</b>\n══════════════════════════\n\n✮ 𝘗𝘰𝘬𝘦𝘮𝘰𝘯/𝘛𝘮 : <b>{pokemon_name}</b>!\n\n▬▬▬▬▬▬▬▬▬▬▬▬ (100%) \n━━━━━━━━━━━━━━━━━━━━━━━━━━"
            f"<blockquote> <i>✅ 𝗬𝗼𝘂𝗿 𝗧𝗠 𝗜𝘀 𝗦𝗲𝗻𝘁 𝗙𝗼𝗿 𝗦𝘂𝗯𝗺𝗶𝘀𝘀𝗶𝗼𝗻!</i>\n"
            f"⏳ <b>📢 𝗔𝗳𝘁𝗲𝗿 𝗔𝗰𝗰𝗲𝗽𝘁 𝗢𝗿 𝗥𝗲𝗷𝗲𝗰𝘁 𝗬𝗼𝘂 𝗪𝗶𝗹𝗹 𝗕𝗲 𝗡𝗼𝘁𝗶𝗳𝗶𝗲𝗱</b>\n</blockquote>"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
    bot.send_message(call.message.chat.id, text+ls , parse_mode='html',reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('AUCTION GROUP', url=AUCTION_GROUP_LINK)))
    bot.send_message(log_channel, text, parse_mode='html', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('APPROVE', callback_data=f'approve_{user_id}'),                                                                                      
                                                                                      types.InlineKeyboardButton('REJECT', callback_data=f'reject_{user_id}'),))

import json

DATA_FILE = "data.json"

# Function to load existing data (or initialize empty lists)
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "crat_id": [],
            "chat_id": [],
            "brat_id": [],
            "craft_id": [],
            "trat_id": [],
            "legpoke_name": [],
            "nonleg_name": [],
            "tmen": [],
            "shineiess": [],
            "teams": [],
            "msg_leg": [],
            "msg_nonleg": [],
            "msg_shiny": [],
            "msg_tm": [],
            "msg_team": [],
        }

# Function to save data back to JSON
def save_data():
    data = {
        "crat_id": crat_id,
        "chat_id": chat_id,
        "brat_id": brat_id,
        "craft_id": craft_id,
        "trat_id": trat_id,
        "legpoke_name": legpoke_name,
        "nonleg_name": nonleg_name,
        "tmen": tmen,
        "shineiess": shineiess,
        "teams": teams,
        "msg_leg": msg_leg,
        "msg_nonleg": msg_nonleg,
        "msg_shiny": msg_shiny,
        "msg_tm": msg_tm,
        "msg_team": msg_team
    }
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load data into lists
data = load_data()
crat_id = data["crat_id"]
chat_id = data["chat_id"]
brat_id = data["brat_id"]
craft_id = data["craft_id"]
trat_id = data["trat_id"]
legpoke_name = data["legpoke_name"]
nonleg_name = data["nonleg_name"]
tmen = data["tmen"]
shineiess = data["shineiess"]
teams = data["teams"]
msg_leg = data["msg_leg"]
msg_nonleg = data["msg_nonleg"]
msg_shiny = data["msg_shiny"]
msg_tm = data["msg_tm"]
msg_team = data["msg_team"]

# Save updated lists back to JSON
save_data()

import json
import os

# Initialize your global variables
users_nich = {}

# File path
USERS_DATA_FILE = "users_ata.json"

def save_users_data():
    try:
        data = {
            "users_nich": users_nich
        }
        with open(USERS_DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("✅ User data saved.")
    except Exception as e:
        print(f"❌ Error saving users_data: {e}")

def load_users_data():
    global users_nich
    if not os.path.exists(USERS_DATA_FILE):
        users_nich = {}
        approved_counts = {}
        print("⚠️ users_ata.json not found. Initialized empty data.")
        return

    try:
        with open(USERS_DATA_FILE, "r") as f:
            data = json.load(f)
            users_nich = data.get("users_nich", {})
        print("✅ User data loaded.")
    except Exception as e:
        print(f"❌ Error loading users_data: {e}")
        users_nich = {}

# Load at startup
load_users_data()

def extract_pokemon_name(message_text):
    """
    Extracts the Pokémon name (e.g., 'dred') from the message text.
    """
    import re

    # Search for the line starting with 'Pokemon Name:' and capture the name
    match = re.search(r"Pokemon Name:\s*(\w+)", message_text)
    if match:
        return match.group(1)  # Return the captured Pokémon name
    return None  # Return None if no Pokémon name is found

def extract_team_details(message_text):
    """
    Extracts the Pokémon name (e.g., 'dred') from the message text.
    """
    import re

    # Search for the line starting with 'Pokemon Name:' and capture the name
    match = re.search(r"Team name:\s*(\w+)", message_text)
    if match:
        return match.group(1)  # Return the captured Pokémon name
    return None  # Return None if no Pokémon name is found

def extract_tm_details(message_text):
    """
    Extracts the TM code (e.g., 'TM13') from the message text.
    """
    import re
    print(message_text)
    # Use a regular expression to find 'TM' followed by digits
    match = re.search(r"TM\d+", message_text, re.IGNORECASE)
    if match:
        return match.group(0)  # Return just 'TM13'
    return None  # Return None if no TM code is found

@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def handle_admin_actions(call):
    user_id = call.from_user.id
    
    data_parts = call.data.split("_")
    call_data = data_parts[0]
    userd = int(data_parts[1])
    
    if user_id in xmods:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        
        if call_data == 'approve':
            # Forward the message
            original_message = bot.forward_message(post_channel, log_channel, call.message.message_id)
            bot.forward_message(approve_channel, log_channel, call.message.message_id)

            # Ensure the message has text or caption content
            if original_message.text:
                message_text = original_message.text # Extract the text content of the message
                
            elif original_message.caption:
                message_text = original_message.caption # Extract the caption if text is None

                # Process based on message content
            if '#Shiny' in message_text:
                chat_id.append(f"https://t.me/aho_hexa_auction/{original_message.message_id}")
                if "Pokemon Name:" in message_text:  # Check for the key in the text
                    pokemon_name = extract_pokemon_name(message_text)  # Extract Pokémon name
                    shineiess.append(pokemon_name)
                    bot.send_message(userd, f"🎉𝘠𝘰𝘶𝘳 **{pokemon_name}** 𝘚𝘶𝘣𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘏𝘢𝘴 𝘉𝘦𝘦𝘯 𝘈𝘱𝘱𝘳𝘰𝘷𝘦𝘥!\n\n🥂𝘊𝘩𝘦𝘤𝘬 𝘉𝘦𝘭𝘰𝘸 𝘍𝘰𝘳 𝘈𝘶𝘤𝘵𝘪𝘰𝘯 𝘎𝘳𝘰𝘶𝘱 𝘓𝘪𝘯k✨",parse_mode='markdown',reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('AUCTION GROUP', url=AUCTION_GROUP_LINK)))
                    try:
                        save_data()
                        users_nich.setdefault(str(userd), {}).setdefault("shiny", []).append({
                            "name": pokemon_name,
                            "link": f"https://t.me/aho_hexa_auction/{original_message.message_id}"
                        })
                        save_users_data()
                    except Exception as e:
                        print(f"[ERROR] Approve item process failed: {e}")

            elif '#Legendary' in message_text:
                crat_id.append(f"https://t.me/aho_hexa_auction/{original_message.message_id}")
                if "Pokemon Name:" in message_text:
                    pokemon_name = extract_pokemon_name(message_text)
                    legpoke_name.append(pokemon_name)
                    bot.send_message(userd, f"🎉𝘠𝘰𝘶𝘳 **{pokemon_name}** 𝘚𝘶𝘣𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘏𝘢𝘴 𝘉𝘦𝘦𝘯 𝘈𝘱𝘱𝘳𝘰𝘷𝘦𝘥!\n\n🥂𝘊𝘩𝘦𝘤𝘬 𝘉𝘦𝘭𝘰𝘸 𝘍𝘰𝘳 𝘈𝘶𝘤𝘵𝘪𝘰𝘯 𝘎𝘳𝘰𝘶𝘱 𝘓𝘪𝘯k✨",parse_mode='markdown',reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('AUCTION GROUP', url=AUCTION_GROUP_LINK)))
                    try:    
                        save_data()
                        users_nich.setdefault(str(userd), {}).setdefault("legendary", []).append({
                            "name": pokemon_name,
                            "link": f"https://t.me/aho_hexa_auction/{original_message.message_id}"
                        })
                        save_users_data()
                    except Exception as e:
                        print(f"[ERROR] Approve item process failed: {e}")

            elif '#Non_legendary' in message_text:
                brat_id.append(f"https://t.me/aho_hexa_auction/{original_message.message_id}")
                if "Pokemon Name:" in message_text:
                    pokemon_name = extract_pokemon_name(message_text)
                    nonleg_name.append(pokemon_name)
                    bot.send_message(userd, f"🎉𝘠𝘰𝘶𝘳 **{pokemon_name}** 𝘚𝘶𝘣𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘏𝘢𝘴 𝘉𝘦𝘦𝘯 𝘈𝘱𝘱𝘳𝘰𝘷𝘦𝘥!\n\n🥂𝘊𝘩𝘦𝘤𝘬 𝘉𝘦𝘭𝘰𝘸 𝘍𝘰𝘳 𝘈𝘶𝘤𝘵𝘪𝘰𝘯 𝘎𝘳𝘰𝘶𝘱 𝘓𝘪𝘯k✨",parse_mode='markdown',reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('AUCTION GROUP', url=AUCTION_GROUP_LINK)))
                    try:
                        save_data()
                        users_nich.setdefault(str(userd), {}).setdefault("nonleg", []).append({
                            "name": pokemon_name,
                            "link": f"https://t.me/aho_hexa_auction/{original_message.message_id}"
                        })
                        save_users_data()
                        print("[DEBUG] Save completed.")
                    except Exception as e:
                        print(f"[ERROR] Approve item process failed: {e}")

            elif 'About TM:' in message_text:
                craft_id.append(f"https://t.me/aho_hexa_auction/{original_message.message_id}")
                tm_name = extract_tm_details(message_text)  # Extract TM code
                if tm_name:
                    tmen.append(tm_name)
                    bot.send_message(userd, f"🎉𝘠𝘰𝘶𝘳 **{tm_name}** 𝘚𝘶𝘣𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘏𝘢𝘴 𝘉𝘦𝘦𝘯 𝘈𝘱𝘱𝘳𝘰𝘷𝘦𝘥!\n\n🥂𝘊𝘩𝘦𝘤𝘬 𝘉𝘦𝘭𝘰𝘸 𝘍𝘰𝘳 𝘈𝘶𝘤𝘵𝘪𝘰𝘯 𝘎𝘳𝘰𝘶𝘱 𝘓𝘪𝘯k✨",parse_mode='markdown',reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('AUCTION GROUP', url=AUCTION_GROUP_LINK)))
                    try:
                        save_data()
                        users_nich.setdefault(str(userd), {}).setdefault("tmn", []).append({
                            "name": tm_name,
                            "link": f"https://t.me/aho_hexa_auction/{original_message.message_id}"
                        })
                        save_users_data()
                        print("[DEBUG] Save completed.")
                    except Exception as e:
                        print(f"[ERROR] Approve item process failed: {e}")

            elif '#Teams' in message_text:
                trat_id.append(f"https://t.me/aho_hexa_auction/{original_message.message_id}")
                team_name = extract_team_details(message_text)  # Extract TM code
                if team_name:
                    teams.append(team_name)
                    bot.send_message(userd, f"🎉𝘠𝘰𝘶𝘳 **{team_name}** 𝘚𝘶𝘣𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘏𝘢𝘴 𝘉𝘦𝘦𝘯 𝘈𝘱𝘱𝘳𝘰𝘷𝘦𝘥!\n\n🥂𝘊𝘩𝘦𝘤𝘬 𝘉𝘦𝘭𝘰𝘸 𝘍𝘰𝘳 𝘈𝘶𝘤𝘵𝘪𝘰𝘯 𝘎𝘳𝘰𝘶𝘱 𝘓𝘪??k✨",parse_mode='markdown',reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('AUCTION GROUP', url=AUCTION_GROUP_LINK)))
                    try:
                        save_data()
                        users_nich.setdefault(str(userd), {}).setdefault("team", []).append({
                            "name": team_name,
                            "link": f"https://t.me/aho_hexa_auction/{original_message.message_id}"
                        })
                        save_users_data()
                    except Exception as e:
                        print(f"[ERROR] Approve item process failed: {e}")

                            
                # Notify approval
            
            bot.send_message(approve_channel, f"Accepted by @{call.from_user.username}")
            
        else:
            
            
            original_message = bot.forward_message(reject_channel, log_channel, call.message.message_id)
            bot.delete_message(log_channel, call.message.message_id)
            
            # Ensure the message has text or caption content
            if original_message.text:
                message_text = original_message.text # Extract the text content of the message
                
            elif original_message.caption:
                message_text = original_message.caption # Extract the caption if text is None

                # Process based on message content
            if '#Shiny' in message_text:
                if "Pokemon Name:" in message_text:  # Check for the key in the text
                    pokemon_name = extract_pokemon_name(message_text)  # Extract Pokémon name
                    item_name = pokemon_name
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('Nature is bad',callback_data=f'rejn_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('ivs is ded ',callback_data=f'rejii_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('main move is missing',callback_data=f'rejm_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('pokemon is ded',callback_data=f'rejdd_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('reject base price is high',callback_data=f'rejb_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('other reason',callback_data=f'rejo_{userd}_{item_name}'))
                    
            elif '#Legendary' in message_text:
                if "Pokemon Name:" in message_text:
                    pokemon_name = extract_pokemon_name(message_text)
                    item_name = pokemon_name
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('Nature is bad',callback_data=f'rejn_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('ivs is ded ',callback_data=f'rejii_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('main move is missing',callback_data=f'rejm_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('pokemon is ded',callback_data=f'rejdd_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('reject base price is high',callback_data=f'rejb_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('other reason',callback_data=f'rejo_{userd}_{item_name}'))
                    
            elif '#Non_legendary' in message_text:
                if "Pokemon Name:" in message_text:
                    pokemon_name = extract_pokemon_name(message_text)
                    item_name = pokemon_name
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton('Nature is bad',callback_data=f'rejn_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('ivs is ded ',callback_data=f'rejii_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('main move is missing',callback_data=f'rejm_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('pokemon is ded',callback_data=f'rejdd_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('reject base price is high',callback_data=f'rejb_{userd}_{item_name}'))
                    markup.add(InlineKeyboardButton('other reason',callback_data=f'rejo_{userd}_{item_name}'))
                    
            elif 'About TM:' in message_text:
                tm_name = extract_tm_details(message_text)  # Extract TM code
                item_name = tm_name  
                markup = InlineKeyboardMarkup() 
                markup.add(InlineKeyboardButton('reject waste tm',callback_data=f'rejt_{userd}_{item_name}'))
                markup.add(InlineKeyboardButton('reject base price is high',callback_data=f'rejb_{userd}_{item_name}'))
                markup.add(InlineKeyboardButton('other reason',callback_data=f'rejo_{userd}_{item_name}'))
                
            elif '#Teams' in message_text:
                team_name = extract_team_details(message_text)  # Extract TM code
                item_name = team_name
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('reject due to high level',callback_data=f'rejh_{userd}_{item_name}'))
                markup.add(InlineKeyboardButton('reject base price is high',callback_data=f'rejb_{userd}_{item_name}'))
                markup.add(InlineKeyboardButton('other reason',callback_data=f'rejo_{userd}_{item_name}'))
                
            bot.send_message(
                reject_channel,
                "Select the reason for rejection",
                reply_markup=markup
            )
                
    else:
        bot.send_sticker(call.message.chat.id, ANGRY_STICKER_ID)
        bot.answer_callback_query(call.id, 'You are not the auctioneer', show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith(("rejii_", "rejn_","rejb_","rejo_","rejt_","rejdd_","rejm_","rejh_")))
def callbacksjiji(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    user_id = call.from_user.id
    dp = call.data.split('_')
    action = dp[0]
    used = int(dp[1])
    itenn = dp[2]
    
    if user_id not in xmods:
        bot.send_sticker(call.message.chat.id, ANGRY_STICKER_ID)
        bot.answer_callback_query(call.id, 'You are not the auctioneer', show_alert=True)
        return
    
    if action == 'rejii':
        text = '<blockquote><b>𝘗𝘰𝘬𝘦𝘮𝘰𝘯 𝘐𝘝 𝘐𝘴 𝘙𝘪𝘱.</b></blockquote>'
    elif action == 'rejn':
        text = '<blockquote><b>𝘗𝘰𝘬𝘦𝘮𝘰𝘯 𝘕𝘢𝘵𝘶𝘳𝘦 𝘐𝘴 𝘙𝘪𝘱.</b></blockquote>'
    elif action == 'rejb':
        text = '<blockquote><b>𝘉𝘢𝘴𝘦 𝘗𝘳𝘪𝘤𝘦 𝘐𝘴 𝘏𝘪𝘨𝘩.</b></blockquote>'
    elif action == 'rejo':
        text = '<blockquote><b>𝘕𝘰 𝘙𝘦𝘢𝘴𝘰𝘯. | 𝘙𝘦𝘢𝘴𝘰𝘯 𝘐𝘴 𝘉𝘭𝘢𝘯𝘬.</b></blockquote>'
    elif action == 'rejt':
        text = '<blockquote><b>𝘜𝘴𝘦𝘭𝘦𝘴𝘴 𝘛𝘮𝘴.</b></blockquote>'
    elif action == 'rejdd':
        text = '<blockquote><b>𝘗𝘰𝘬𝘦𝘮𝘰𝘯 𝘐𝘴 𝘜𝘴𝘦𝘭𝘦𝘴𝘴.</b></blockquote>'
    elif action == 'rejm':
        text = '<blockquote><b>𝘗𝘰𝘬𝘦𝘮𝘰𝘯`𝘴 𝘔𝘢𝘪𝘯 𝘔𝘰𝘷𝘦 𝘐𝘴 𝘔𝘪𝘴𝘴𝘪𝘯𝘨.</b></blockquote>'
    elif action == 'rejh':
        text = '<blockquote><b>𝘛𝘦𝘢𝘮𝘴 𝘓𝘦𝘷𝘦𝘭 𝘐𝘴 𝘏𝘪𝘨𝘩.</b></blockquote>'
        
    bat = (
        "🔴 Rejected \n"
        f"<b>📣 Item Name: {itenn}\n</b>"
        f"<b>💬 Reason:\n\n</b>"
    )
    bot.send_message(
        reject_channel,
        bat+text,
        parse_mode='html'
    )
    
    bot.send_message(
        used,
        bat+text,
        parse_mode='html'
    )

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.message_handler(commands=['myitem'])
def myitem(message):
    user_id = str(message.from_user.id)
    if user_id not in users_nich:
        bot.reply_to(message, "No items found for your ID.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✨ Shiny", callback_data=f"myitem_shiny_{user_id}"),
        InlineKeyboardButton("🌟 Legendary", callback_data=f"myitem_legendary_{user_id}"),
        InlineKeyboardButton("🔹 Non-Legendary", callback_data=f"myitem_nonleg_{user_id}"),
        InlineKeyboardButton("📘 TMs", callback_data=f"myitem_tmn_{user_id}"),
        InlineKeyboardButton("👥 Teams", callback_data=f"myitem_team_{user_id}")
    )
    markup.add(InlineKeyboardButton("❌ Close", callback_data=f"close_{user_id}"))

    bot.reply_to(message, "📦 Select a category to view your approved items:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("myitem_"))
def show_myitem_category(call):
    _, category, user_id = call.data.split("_", 2)

    if call.from_user.id != int(user_id):
        bot.answer_callback_query(call.id, "This menu isn't for you.")
        return

    if user_id not in users_nich:
        bot.edit_message_text("No items found for your ID.", call.message.chat.id, call.message.message_id)
        return

    user_items = users_nich[user_id]
    items = user_items.get(category, [])

    if not items:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔙 Back to Menu", callback_data=f"myite_menu_{user_id}"),
            InlineKeyboardButton("❌ Close", callback_data=f"close_{user_id}")
        )
        bot.edit_message_text(f"No {category.title()} items found.", call.message.chat.id, call.message.message_id,reply_markup=markup)
        return

    title_map = {
        "shiny": "✨ Shiny Pokémon",
        "legendary": "🌟 Legendary Pokémon",
        "nonleg": "🔹 Non-Legendary Pokémon",
        "tmn": "📘 TMs",
        "team": "👥 Teams"
    }

    text = f"{title_map.get(category, category.title())}:\n\n"
    for item in items:
        name = item.get("name", "Unnamed")
        link = item.get("link", "#")
        text += f"  ◾ [{name}]({link})\n"

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔙 Back to Menu", callback_data=f"myite_menu_{user_id}"),
        InlineKeyboardButton("❌ Close", callback_data=f"close_{user_id}")
    )

    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("myite_menu_"))
def back_to_menu(call):
    user_id = call.data.split("_")[-1]

    if call.from_user.id != int(user_id):
        bot.answer_callback_query(call.id, "This menu isn't for you.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✨ Shiny", callback_data=f"myitem_shiny_{user_id}"),
        InlineKeyboardButton("🌟 Legendary", callback_data=f"myitem_legendary_{user_id}"),
        InlineKeyboardButton("🔹 Non-Legendary", callback_data=f"myitem_nonleg_{user_id}"),
        InlineKeyboardButton("📘 TMs", callback_data=f"myitem_tmn_{user_id}"),
        InlineKeyboardButton("👥 Teams", callback_data=f"myitem_team_{user_id}")
    )
    markup.add(InlineKeyboardButton("❌ Close", callback_data=f"close_{user_id}"))

    bot.edit_message_text("📦 Select a category to view your approved items:",
                          call.message.chat.id, call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("close_"))
def close_menu(call):
    user_id = call.data.split("_")[1]
    if call.from_user.id != int(user_id):
        bot.answer_callback_query(call.id, "This menu isn't for you.")
        return
    bot.delete_message(call.message.chat.id, call.message.message_id)

def elements_items_list(chat_id, msg_id):
    photo = 'https://i.postimg.cc/CLcgF4WM/IMG-20241226-182420-618.jpg'
    text = "welcome to items page \n click any button to check in your desire:"
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('shiny', callback_data='shini'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('Teams', callback_data='team'),
            types.InlineKeyboardButton('Back', callback_data='back')
        )

    sendoff = bot.send_photo(
            chat_id,
            photo=photo,
            caption=text,
            reply_markup=markup,
            reply_to_message_id=msg_id
        )
    return sendoff.message_id

@bot.message_handler(commands=['elements'])
def send_detuils(message):
    user_id = message.from_user.id
    if not has_started_bot(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
        bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    if not is_user_updated(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('update',url='https://t.me/Auct_he_bot?start=update'))
        bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    message_id = elements_items_list(message.chat.id, message.message_id)   

def create_hyperlink(name, link):
    template = Template("<a href='{{ link }}'>{{ name }}</a>")
    html = template.render(name = name, link= link) 
    return html

vari = []
bari = []
nari = []
lari = []
gari = []
    
def legendary_ele(call):
    if len(legpoke_name) == 0:
        text = "No legendary Pokémon are added yet."
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('Back', callback_data='back'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('Shiny', callback_data='shini'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('teams', callback_data='team')
        )
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=text,
            reply_markup=markup
        )
    else:
        text = "🔥 Welcome to the Legendary Page!\n\nThe legendary Pokémon of the auction are:"
        
        # Ensure crat_id is iterable
        crat = [f"{j}" for j in crat_id]
        
        # Use zip to pair each Pokémon name with a corresponding crat_id link
        combined_links = zip(legpoke_name, crat)
        
        # Create unique hyperlinks and store them in vari
        vari.extend(
            create_hyperlink(name, link)
            for name, link in combined_links
            if create_hyperlink(name, link) not in vari
        )
        
        # Append each unique hyperlink to the text
        for k in vari:
            text += f'\n⚜️ {k}'

        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('Back', callback_data='back'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('Shiny', callback_data='shini'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('teams', callback_data='team')
        )
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=text,
            reply_markup=markup,
            parse_mode='HTML'  # Use HTML for hyperlink formatting
        )

    
def nonleg_ele(call):
    if len(nonleg_name) == 0:
        text = "no non_legendary pokemons are added yet"
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('back', callback_data='back'),
            types.InlineKeyboardButton('shiny', callback_data='shini'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('teams', callback_data='team')
        )
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption= text,
            reply_markup=markup
              # Use strict MarkdownV2 mode
            )
    
    else:    
        text = "🔥 Welcome to the Non-Legendary Page!\n\nthe Non-Legendary pokemons of the auction:-"
        crat = [f"{j}" for j in brat_id]
        
        combined_links = zip(nonleg_name, crat)
        bari.extend(
            create_hyperlink(name, link)
            for name, link in combined_links
            if create_hyperlink(name, link) not in bari
        )

        for k in bari:
            text += f'\n💠 {k}'
        
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('Back', callback_data='back'),
            types.InlineKeyboardButton('shiny', callback_data='shini'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('teams', callback_data='team')
        )
        bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=text,
                reply_markup=markup,
                parse_mode='HTML'
                # Use strict MarkdownV2 mode
            )

def shiny_ele(call):
    if len(shineiess) == 0:
        text = "no shinies are added yet"
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('back', callback_data='back'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('teams', callback_data='team')
        )
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption= text,
            reply_markup=markup
             # Use strict MarkdownV2 mode
            )
     
    else:    
        text = "🔥 Welcome to the shiny Page!\n\nthe shiny pokemons of the auction:-"
        crat = [f"{j}" for j in chat_id]

        combined_links = zip(shineiess, crat)
        nari.extend(
            create_hyperlink(name, link)
            for name, link in combined_links
            if create_hyperlink(name, link) not in nari
        )

        for k in nari:
            text += f'\n✨ {k}'
            
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('back', callback_data='back'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('teams', callback_data='team')
        )
        bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=text,
                reply_markup=markup,
                parse_mode='HTML'# Use strict MarkdownV2 mode
            )
    
def tm_ele(call):
    if len(tmen) == 0:
        text = "No TMs are added yet."
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('shiny', callback_data='shini'),
            types.InlineKeyboardButton('back', callback_data='back'),
            types.InlineKeyboardButton('teams', callback_data='team')
        )
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=text,
            reply_markup=markup
        )
    else:
        text = "🔥 Welcome to the TMs Page!\n\nThe TMs Pokémons of the auction are:"
        crat = [f"{j}" for j in craft_id]

        combined_links = zip(tmen, crat)
        lari.extend(
            create_hyperlink(name, link)
            for name, link in combined_links
            if create_hyperlink(name, link) not in lari
        )

        for k in lari:
            text += f'\n🔹 {k}'

        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('shiny', callback_data='shini'),
            types.InlineKeyboardButton('back', callback_data='back'),
            types.InlineKeyboardButton('teams', callback_data='team')
        )
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=text,
            reply_markup=markup,
            parse_mode='HTML'  # Use HTML for hyperlink formatting
        )
        
def team_ele(call):
    if len(teams) == 0:
        text = "No Teams are added yet."
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('shiny', callback_data='shini'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('back', callback_data='back')
        )
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=text,
            reply_markup=markup
        )
    else:
        text = "🔥 Welcome to the TMs Page!\n\nThe TMs Pokémons of the auction are:"
        crat = [f"{j}" for j in trat_id]

        combined_links = zip(teams, crat)
        gari.extend(
            create_hyperlink(name, link)
            for name, link in combined_links
            if create_hyperlink(name, link) not in gari
        )

        for k in gari:
            text += f'\n🔹 {k}'

        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton('6ls', callback_data='lls'),
            types.InlineKeyboardButton('0ls', callback_data='pls'),
            types.InlineKeyboardButton('shiny', callback_data='shini'),
            types.InlineKeyboardButton('TMs', callback_data='tme'),
            types.InlineKeyboardButton('back', callback_data='back')
        )
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=text,
            reply_markup=markup,
            parse_mode='HTML'  # Use HTML for hyperlink formatting
        )

@bot.message_handler(commands=['reseti'])
def reset_all_lists(message):
    """Clears all stored lists (Admin-Only)."""
    if message.from_user.id not in xmods:
        bot.reply_to(message, "❌ You do not have permission to use this command.")
        return

    global lari, vari, nari, bari, gari
    global legpoke_name, nonleg_name, shineiess, tmen, teams
    global brat_id, crat_id, chat_id, craft_id, trat_id
    global msg_leg, msg_nonleg, msg_shiny, msg_tm, msg_team

    # Reset all lists
    nari.clear()
    bari.clear()
    lari.clear()
    vari.clear()
    gari.clear()

    legpoke_name.clear()
    nonleg_name.clear()
    shineiess.clear()
    tmen.clear()
    teams.clear()

    brat_id.clear()
    crat_id.clear()
    chat_id.clear()
    craft_id.clear()
    trat_id.clear()
    
    msg_leg.clear()
    msg_nonleg.clear()
    msg_shiny.clear()
    msg_tm.clear()
    msg_team.clear()
    
    save_data()
    
    users_nich.clear()
    save_users_data()

    bot.reply_to(message, "✅ All Pokémon lists, names, and IDs have been **cleared** successfully!",parse_mode='markdown')

@bot.message_handler(commands=['limpokes'])
def list_pokemon_counts(message):
    
    if message.from_user.id not in xmods:
        bot.reply_to(message, "❌ You do not have permission to use this command.")
        return
    
    """Displays the count of Pokémon & TMs in the auction with progress bars."""
    
    total_limit = 100
    category_limits = {"legendary": 20, "non-legendary": 50, "shiny": 10, "tms": 15, "teams": 5}

    # Current counts
    current_counts = {
        "legendary": len(legpoke_name),
        "non-legendary": len(nonleg_name),
        "shiny": len(shineiess),
        "tms": len(tmen),
        "teams": len(teams)
    }

    # Function to create progress bars
    def progress_bar(count, limit, bar_length=10):
        filled = round((count / limit) * bar_length)
        return "▰" * filled + "▱" * (bar_length - filled)

    # Format message
    message_text = (
        "<b>📜 CURRENT AUCTION STATUS 📜</b>\n"
        "<i>Here's the count of Pokémon & TMs currently in the auction:</i>\n\n"
        "🟡 <b>Legendary Pokémon:</b> {}/20\n"
        "   [{}]\n"
        "🔵 <b>Non-Legendary Pokémon:</b> {}/50\n"
        "   [{}]\n"
        "✨ <b>Shiny Pokémon:</b> {}/10\n"
        "   [{}]\n"
        "📜 <b>TMs:</b> {}/15\n"
        "   [{}]\n"
        "🏹 <b>Teams:</b> {}/5\n"
        "   [{}]\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>Total Pokémon & TMs:</b> {}/100\n"
        "   [{}]\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    ).format(
        current_counts["legendary"], progress_bar(current_counts["legendary"], category_limits["legendary"]),
        current_counts["non-legendary"], progress_bar(current_counts["non-legendary"], category_limits["non-legendary"]),
        current_counts["shiny"], progress_bar(current_counts["shiny"], category_limits["shiny"]),
        current_counts["tms"], progress_bar(current_counts["tms"], category_limits["tms"]),
        current_counts["teams"], progress_bar(current_counts["teams"], category_limits["teams"]),
        sum(current_counts.values()), progress_bar(sum(current_counts.values()), total_limit)
    )

    bot.reply_to(message, message_text, parse_mode="HTML")

import re
from difflib import get_close_matches
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Combine all into one list
def get_all_pokemon_links():
    return vari + bari + nari + lari + gari

# Extract name and link from HTML anchor tag
def parse_html_link(html_string):
    match = re.search(r"<a href=['\"](.*?)['\"]>(.*?)</a>", html_string)
    if match:
        return match.group(2), match.group(1)  # name, link
    return None, None

@bot.message_handler(commands=['info'])
def info_command(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Please provide a Pokémon name.\nUsage: `/info charizard`", parse_mode="Markdown")
        return

    query = args[1].strip().lower()
    all_links = get_all_pokemon_links()

    # Parse all into (name, link) tuples
    parsed_data = [parse_html_link(x) for x in all_links if parse_html_link(x)[0]]

    # Find all exact matches (case-insensitive)
    matches = [(name, link) for name, link in parsed_data if name.lower() == query]

    if matches:
        mes = bot.reply_to(message, "⏳ Please wait, checking...")
        time.sleep(2)
        return send_multiple_info(mes.chat.id, mes.message_id, query, matches)

    # If no exact match, suggest similar ones
    names = [name for name, _ in parsed_data]
    close_matches = get_close_matches(query, names, n=5, cutoff=0.5)

    if close_matches:
        markup = InlineKeyboardMarkup()
        for name in close_matches:
            markup.add(InlineKeyboardButton(text=name, callback_data=f"info:{name.lower()}"))
        bot.reply_to(message, f"❌ No exact match found for *{query}*.\n\nDid you mean one of these?", parse_mode="Markdown", reply_markup=markup)
    else:
        bot.reply_to(message, f"❌ No match or suggestion found for *{query}*.", parse_mode="Markdown")

# Send multiple results if same name found more than once
def send_multiple_info(chat_id, message_id, name, matches):
    text = f"🔍 Info for <b>{name.title()}</b>:\n"
    markup = InlineKeyboardMarkup()
    for i, (n, link) in enumerate(matches, start=1):
        text += f"{i}. <a href='{link}'>{n}</a>\n"
        markup.add(InlineKeyboardButton(f"📨 View Message {i}", url=link))

    bot.edit_message_text(
        text,
        chat_id,
        message_id,
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=True
    )

# Callback from close match buttons
@bot.callback_query_handler(func=lambda call: call.data.startswith("info:"))
def handle_info_callback(call):
    name_query = call.data.split("info:", 1)[1].lower()
    parsed_data = [parse_html_link(x) for x in get_all_pokemon_links() if parse_html_link(x)[0]]
    matches = [(name, link) for name, link in parsed_data if name.lower() == name_query]

    if matches:
        send_multiple_info(call.message.chat.id, call.message.message_id, name_query, matches)
    else:
        bot.answer_callback_query(call.id, "❌ Pokémon not found.")

@bot.message_handler(commands=['msg'])
def handle_msg(message):
    # Check if the user is banned
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You are banned by an administrator.")
        return

    # Check if the user is an authorized admin
    if message.from_user.id not in admin_id:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    # Parse the command arguments
    try:
        _, user_id, user_message = message.text.split(maxsplit=2)
        user_id = int(user_id)  # Convert user_id to an integer
    except ValueError:
        bot.reply_to(message, "Invalid syntax. Use: /msg <user_id> <message>")
        return

    # Attempt to send the message to the specified user
    try:
        bot.send_message(user_id, user_message)
        bot.reply_to(message, f"Message successfully sent to user {user_id}.")
    except Exception as e:
        bot.reply_to(message, f"Failed to send message to user {user_id}. Error: {e}")
        
@bot.message_handler(commands=['rules'])
def rule_page(message):
    user_id = message.from_user.id
    if not has_started_bot(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
        bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    if not is_user_updated(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('update',url='https://t.me/Auct_he_bot?start=update'))
        bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    image = 'https://i.imghippo.com/files/WDS1997ELI.jpg'
    text = (
        "<b> 📌 RULES </b>\n"
        "〄╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍\n\n"
        "➥ 𝘞𝘩𝘪𝘤𝘩 𝘙𝘶𝘭𝘦𝘴 𝘠𝘰𝘶 𝘸𝘢𝘯𝘵 𝘛𝘰 𝘊𝘩𝘦𝘤𝘬?"
        )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
            types.InlineKeyboardButton('AUCTION', callback_data='auced'),
            types.InlineKeyboardButton('COMMUNITY', callback_data='comed'),
            types.InlineKeyboardButton('🔗 MAIN GROUP LINK', url='https://t.me/AllinoneHexa'))
    
    bot.send_photo(
        message.chat.id,
        photo=image,
        caption=text,
        reply_to_message_id=message.message_id,
        reply_markup=markup,
        parse_mode='html'
    )

@bot.callback_query_handler(func=lambda call: call.data == "comed")
def comed(call):
    tex = (
        """<blockquote>╭═══════════════════════
✮ COMMUNITY RULES ✨
╰━━━━━━━━━━━━━━━━━━━━━━━
➥ ғᴏʀ ᴀɴʏ ᴋɪɴᴅ ᴏғ ᴘʀᴏᴍᴏs ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴs. 
➥ ᴅᴏɴ'ᴛ ᴀʙᴜsᴇ ᴀɴʏᴏɴᴇ. 
➥ ʙᴇ ғʀɪᴇɴᴅʟʏ ᴡɪᴛʜ ᴇᴠᴇʀʏᴏɴᴇ. 
➥ ᴅᴏɴ'ᴛ sᴘᴀᴍ ɪɴ ᴏᴜʀ ɢʀᴏᴜᴘs. 
➥ 𝟷𝟾+ ᴄᴏɴᴛᴇɴᴛs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪɴ ᴏᴜʀ ɢʀᴏᴜᴘ. 
━━━━━━━━━━━━━━━━━━━━━━━━
➥ ɪғ ʏᴏᴜ ɢᴏᴛ ᴀɴʏ sᴄᴀᴍ. 
➥ ɪғ ᴀɴʏᴏɴᴇ ᴀʙᴜsᴇ ʏᴏᴜ. 
➥ ᴀɴʏ ᴏᴛʜᴇʀ ɪssᴜᴇs?⚡️ ᴜsᴇ /𝗛𝗲𝗹𝗽.
  -- 𝘖𝘯𝘭𝘺 𝘞𝘪𝘵𝘩 𝘗𝘳𝘰𝘰𝘧 𝘈𝘤𝘤𝘦𝘱𝘵𝘦𝘥 --</blockquote>"""
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
            types.InlineKeyboardButton('AUCTION', callback_data='auced'),
            types.InlineKeyboardButton('🔗 LINK', url='https://t.me/AIO_COMMUNITY'))
    
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption = tex,
        parse_mode='html',
        reply_markup=markup
    )
    
@bot.callback_query_handler(func=lambda call: call.data == "auced")
def auced(call):
    tex = (
        """<blockquote>╭═══════════════════════
☀️AUCTION RULES ✨
╰━━━━━━━━━━━━━━━━━━━━━━━
▫️ɪғ ᴜ ᴀᴅᴅ ᴀɴʏ ᴘᴏᴋᴇ/ᴛᴍ ɪɴ ᴀᴜᴄᴛɪᴏɴ ᴀɴᴅ ʟᴀᴛᴇʀ ᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴛʜᴀᴛ ᴘᴏᴋᴇ/ᴛᴍ ʙᴇғᴏʀᴇ ᴀᴜᴄᴛɪᴏɴ ᴜ ɢɪᴠᴇ ғɪɴᴇ 𝟒𝐊 ᴘᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴛʜᴀᴛ ᴘᴏᴋᴇ/ᴛᴍ.

▫️ɪғ ᴜ ʙɪᴅ ɪɴ ᴀᴜᴄᴛɪᴏɴ ᴀɴᴅ ʟᴀᴛᴇʀ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴛᴀᴋᴇ ᴛʜᴀᴛ ɪᴛᴇᴍ ᴜ ɢᴏᴛ ᴡᴀʀɴ ᴏʀ ʙᴀɴ ᴀɴᴅ ᴏᴛʜᴇʀ ᴏᴘᴛɪᴏɴ ɪs ɢɪᴠᴇ ғɪɴᴇ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ʙɪᴅ 𝟒𝟎% ғɪɴᴇ ᴘᴀɪᴅ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴ. 

▫️ᴀғᴛᴇʀ ᴀᴜᴄᴛɪᴏɴ ɪғ sᴇʟʟᴇʀ ᴅᴏɴ'ᴛ ɢɪᴠᴇ ᴀɴʏ ɪᴛᴇᴍs ᴛᴏ ᴛʜᴇ ʙᴜʏᴇʀ ʜᴇ ɢᴏᴛ ʙᴀɴ ᴏʀ ᴡᴀʀɴɪɴɢ ᴀɴᴅ ᴏᴛʜᴇʀ ᴏᴘᴛɪᴏɴ ɪs ɢɪᴠᴇ 𝟒𝟎% ғɪɴᴇ ᴏғ ᴛʜᴀᴛ ɪᴛᴇᴍs sᴏʟᴅ ɪɴ ᴀᴜᴄᴛɪᴏɴ. 

▫️ɪғ ᴀɴʏ ᴘʟᴀʏᴇʀ ᴡᴀɴᴛs ᴛᴏ ʀᴇʙɪᴅ ᴏғ ᴛʜᴇɪʀ ɪᴛᴇᴍs ᴛᴇʟʟ ᴀᴅᴍɪɴ ɪɴ ᴛʀᴀᴅᴇ ɢᴄ ᴡʜᴇɴ ᴀᴜᴄᴛɪᴏɴ ɪs ʀᴜɴɴɪɴɢ ᴛʜᴀᴛ ᴛɪᴍᴇ ᴀғᴛᴇʀ ᴀᴜᴄᴛɪᴏɴ ᴜ ʜᴀᴠᴇ ᴀʟsᴏ 𝟷𝟻 ᴍɪɴᴜᴛᴇs  ᴛᴏ ʀᴇʙɪᴅ ᴛʜᴀᴛ ɪᴛᴇᴍs ᴀғᴛᴇʀ ᴛʜᴀᴛ ᴛɪᴍᴇ ᴅᴏɴ'ᴛ ᴅᴏ ʀʀ ᴡɪᴛʜ ᴀᴅᴍɪɴ. 

▫️ɪғ ᴀɴʏ sᴇʟʟᴇʀ ᴅᴏ ʀᴇʙɪᴅ ᴏғ ᴛʜᴇɪʀ ɪᴛᴇᴍs ʟᴀᴛᴇʀ ᴏʟᴅ ʙᴜʏᴇʀ ᴅᴏɴ'ᴛ ᴅᴏ ʀʀ ᴡɪᴛʜ ᴀᴅᴍɪɴ ᴀʙᴏᴜᴛ ᴛʜᴀᴛ ɪᴛᴇᴍs.

➥ ᴀɴʏᴏɴᴇ ᴅᴏɴ'ᴛ ғᴏʟʟᴏᴡ ᴀʙᴏᴠᴇ ʀᴜʟᴇs ʜᴇ ɢᴏᴛ 𝟸 ᴡᴀʀɴs ᴛʜᴇɴ ᴅɪʀᴇᴄᴛ ʙᴀɴ.

➥ ɪғ ᴀɴʏᴏɴᴇ ᴅɪᴅ sᴄᴀᴍ ᴛᴀɢ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴘʀᴏᴏғ.
━━━━━━━━━━━━━━━━━━━━━━━━
✮ ɪɴᴄʀᴇᴀsᴇ ʏᴏᴜʀ ʙɪᴅ ᴡɪᴛʜ ᴍɪɴɪᴍᴜᴍ 𝟓𝟎𝟎 𝐏𝐝. (ᴇxᴄᴇᴘᴛ 𝐓𝐦𝐬)</blockquote>"""
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
            types.InlineKeyboardButton('🔗 LINK', url='https://t.me/allinoneAuction'),
            types.InlineKeyboardButton('COMMUNITY', callback_data='comed'))
    
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption = tex,
        parse_mode='html',
        reply_markup=markup
    )

message_store = {}
stored_messages = {}
current_index = 0
sold_items = []
confirmed_messages = set()

@bot.message_handler(commands=['renext'])
def renext(message):
    global c
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if is_admin(message.from_user.id):
            bot.reply_to(message, "<blockquote>Done reseted next</blockquote>",parse_mode="html")
            c=0
            return
        
@bot.message_handler(commands=['store'])
def store_message_prompt(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if is_admin(message.from_user.id):
            bot.reply_to(message, "<blockquote>Type the message you want to store:</blockquote>",parse_mode="html")
            bot.register_next_step_handler(message, store_message)
        else:
            bot.send_sticker(message.chat.id,ANGRY_STICKER_ID)
            bot.reply_to(message, "<blockquote>Only admins can perform this action.</blockquote>",parse_mode="html")

def store_message(message):
    stored_messages[message.message_id] = {"message": message.text, "chat_id": message.chat.id}
    bot.reply_to(message, "<blockquote>Message stored successfully.</blockquote>",parse_mode="html")

import time
import telebot
from telebot import types

banned_users=[]
auce_active = False  # Track auction status
current_category = None  # Track current auction category

expic = 'https://files.catbox.moe/t9s3sa.jpg'
def extract_seller_details(forwarded_message):
    """
    Extracts the seller's ID and username from the forwarded auction message.
    """
    text = forwarded_message.text if forwarded_message.text else ""
    caption = forwarded_message.caption if forwarded_message.caption else ""

    # Extract User ID
    user_id_match = re.search(r"(?:User ID|User id)[:\s-]+(\d+)", caption + text, re.IGNORECASE)
    seller_id = user_id_match.group(1) if user_id_match else "Unknown ID"

    # Extract Username
    username_match = re.search(r"(?:Username|username)[:\s@]+([\w\d_]+)", caption + text, re.IGNORECASE)
    seller_username = f"@{username_match.group(1)}" if username_match else "Unknown Username"

    return seller_id, seller_username

# ---- START AUCTION COMMAND ----
@bot.message_handler(commands=['aucon'])
def aucon(message):
    chat_id = message.chat.id
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
        return

    if str(message.from_user.id) in admin_ids:
        global auce_active
        if not auce_active:
            auce_active = True
            msg = bot.send_photo(chat_id,photo='https://i.imghippo.com/files/P6359OgI.jpg', caption="Auction is starting....",reply_to_message_id=message.message_id)
            time.sleep(3.5)
            bot.edit_message_caption('🫧 Processing....', chat_id, msg.message_id)
            time.sleep(2.5)
            bot.edit_message_caption('Auction started 💫⚡️', chat_id, msg.message_id)
            time.sleep(1.5)
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🟡 Legendary Pokémon", callback_data="auc_leg"),
                types.InlineKeyboardButton("🔵 Non-Legendary Pokémon", callback_data="auc_nonleg"),
                types.InlineKeyboardButton("✨ Shiny Pokémon", callback_data="auc_shiny"),
                types.InlineKeyboardButton("📜 TMs", callback_data="auc_tm"),
                types.InlineKeyboardButton("🏹 Teams", callback_data="auc_team"),
                types.InlineKeyboardButton("🔙 Back", callback_data="auc_bye")  # No callback for back button
            )
            bot.edit_message_caption('Admins can now select a category to start the auction.', chat_id, msg.message_id, reply_markup = markup)

            

            # Send category selection buttons
        else:
            bot.reply_to(message, "<blockquote>Auction is already active.</blockquote>", parse_mode="HTML")
    else:
        bot.reply_to(message, "<blockquote>Only admins can perform this action.</blockquote>", parse_mode="HTML")

# ---- STOP AUCTION COMMAND ----
@bot.message_handler(commands=['aucoff'])
def aucoff(message):
    chat_id = message.chat.id
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
        return

    if str(message.from_user.id) in admin_ids:
        global auce_active, current_category
        if auce_active:
            auce_active = False
            msg = bot.send_photo(chat_id,photo='https://i.imghippo.com/files/tJ3639N.jpg', caption="Auction is stopping....",reply_to_message_id=message.message_id)
            time.sleep(3)
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("TRADE GROUP", url='https://t.me/allinonehexa'))
            text = "Thanks everyone for participating! Trade Group to see the buyers list."
            bot.edit_message_caption(caption=text, chat_id=chat_id, message_id=msg.message_id, parse_mode="html",reply_markup=markup)
            current_category = None  # Reset category
        else:
            bot.reply_to(message, "<blockquote>Auction is already off.</blockquote>", parse_mode="HTML")
    else:
        bot.reply_to(message, "<blockquote>Only admins can perform this action.</blockquote>", parse_mode="HTML")

# ---- HANDLE CATEGORY SELECTION ----
@bot.callback_query_handler(func=lambda call: call.data.startswith("auc_"))
def handle_auction_category(call):
    
    if call.from_user.id not in xmods:
        bot.answer_callback_query(call.id, text="🖕")
        return
    
    global current_category,c
    c=0

    category = call.data
    if category == "auc_leg":
        current_category = msg_leg
        title = "🟡 Legendary Pokémon"
            
    elif category == "auc_nonleg":
        current_category = msg_nonleg
        title = "🔵 Non-Legendary Pokémon"
            
    elif category == "auc_shiny":
        current_category = msg_shiny
        title = "✨ Shiny Pokémon"
            
    elif category == "auc_tm":
        current_category = msg_tm
        title = "📜 TMs"
        
    elif category == "auc_team":
        current_category = msg_team
        title = "🏹 Teams"
        
    elif category == "auc_bye":
        bot.edit_message_caption(f"Auction ended! ", call.message.chat.id, call.message.message_id)

    bot.answer_callback_query(call.id, "selected!")
    bot.edit_message_caption(f"{title} auction has started!", call.message.chat.id, call.message.message_id)
    next_message(call.message)
    print(f"Category changed to: {title}")  # Debugging log
    
poke_pros = False
brond = True

def next_message(message):
    global current_category
    global c
    global poke_pros
    global brond 

    a = bot.send_message(message.chat.id, "Item loading....")
    time.sleep(2)
    for i in ['3','2','1']:
        bot.edit_message_text(chat_id=a.chat.id,message_id=a.message_id,text=f'sending Item in {i}')
        time.sleep(1)

    bot.delete_message(a.chat.id,a.message_id)

    if current_category:
        try:
            print("here")
            for i in current_category:
                if brond == True:
                    print("here")
                    forwarded_msg = bot.forward_message(message.chat.id, approve_channel, current_category[c])
                    print("sent")
                    brond = False
                    poke_pros = True
                    chat_id = message.chat.id
                        
                        # Send Pokémon/TM name separately
                    c += 1
                    auction_details = extract_pokemon_details(forwarded_msg)
                    print(auction_details)
                    item_name = (
                    auction_details.get("tm_name") or
                    auction_details.get("pokemon_name") or
                    auction_details.get("team_name") or
                    "Unknown Item"
                    )
                    print(item_name)

                    # Send Pokémon/TM name separately
                    bot.send_message(chat_id, f"Next Pokémon/TM: {item_name}", parse_mode='Markdown')
                        
                    message_stor[chat_id] = {
                        "auction_message" : forwarded_msg
                    }
                        # Ensure category is correctly extracted
                    category = auction_details.get("category", "Unknown Category")

                        # ✅ Store auction details with full details

                        # Store the forwarded auction details for use in dot (.) process
                    message_store[chat_id] = {
                    "item_name": (
                        auction_details.get("tm_name") or
                        auction_details.get("pokemon_name") or
                        auction_details.get("team_name") or
                        "Unknown Item"
                    ),
                    "category": auction_details.get("category", "Unknown"),
                    }
                    print(message_store[chat_id])

        except IndexError:
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🟡 Legendary Pokémon", callback_data="auc_leg"),
                InlineKeyboardButton("🔵 Non-Legendary Pokémon", callback_data="auc_nonleg"),
                InlineKeyboardButton("✨ Shiny Pokémon", callback_data="auc_shiny"),
                InlineKeyboardButton("📜 TMs", callback_data="auc_tm"),
                InlineKeyboardButton("🏹 Teams", callback_data="auc_team"),
                InlineKeyboardButton("🔙 Back", callback_data="auc_bye")  # No callback for back button
            )
            bot.send_photo(message.chat.id,photo=expic,caption= "<blockquote>No more Pokémon in this category.\n choose next category from below options</blockquote>", parse_mode="html",reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
                InlineKeyboardButton("🟡 Legendary Pokémon", callback_data="auc_leg"),
                InlineKeyboardButton("🔵 Non-Legendary Pokémon", callback_data="auc_nonleg"),
                InlineKeyboardButton("✨ Shiny Pokémon", callback_data="auc_shiny"),
                InlineKeyboardButton("📜 TMs", callback_data="auc_tm"),
                InlineKeyboardButton("🏹 Teams", callback_data="auc_team"),
                InlineKeyboardButton("🔙 Back", callback_data="auc_bye")  # No callback for back button
            )
        bot.send_photo(message.chat.id,photo=expic,caption= "<blockquote>select the category again.</blockquote>", parse_mode="html",reply_markup=markup)
        
import re

def extract_pokemon_details(forwarded_message):
    """
    Extracts Pokémon, TM, and Team details from a forwarded auction message.
    - Pokémon details are in the caption.
    - TM and Team details are in the text.
    """
    
    if forwarded_message.text:
        message_text = forwarded_message.text
    elif forwarded_message.caption:
        message_text = forwarded_message.caption
    else:
        return None  # No text or caption, return None

    # ✅ Check for TMs
    if "#TMS" in message_text:
        category = "TMS"

        # Extract TM Name
        tm_match = re.search(r"(TM\d+\s+💿)", message_text)
        tm_name = tm_match.group(1).strip() if tm_match else "Unknown TM"

        # Extract Move Name and Type
        move_match = re.search(r"([\w\s]+)\s*\[(.*?)\]", message_text)
        move_name = move_match.group(1).strip() if move_match else "Unknown Move"
        move_type = move_match.group(2).strip() if move_match else "Unknown Type"

        # Extract Power and Accuracy
        power_match = re.search(r"Power:\s*(\d+)", message_text)
        accuracy_match = re.search(r"Accuracy:\s*(\d+)", message_text)
        power = power_match.group(1) if power_match else "N/A"
        accuracy = accuracy_match.group(1) if accuracy_match else "N/A"

        return {
            "category": category,
            "tm_name": tm_name,
            "move_name": move_name,
            "move_type": move_type,
            "power": power,
            "accuracy": accuracy,
        }


    # ✅ Check for Teams
    elif "#Teams" in message_text:
        category = "Teams"

        # Extract Team Name
        team_match = re.search(r"Team name:\s*(.+)", message_text)
        team_name = team_match.group(1).strip() if team_match else "Unknown Team"

        # Extract Pokémon in Team (Only First Line)
        team_pokemon_match = re.search(r"About Team:\s*(.*)", message_text)
        team_pokemon = team_pokemon_match.group(1).split("\n")[0].strip() if team_pokemon_match else "Unknown Pokémon"


        return {
            "category": category,
            "team_name": team_name,
            "team_pokemon": team_pokemon,
        }

    # ✅ Check for Pokémon
    else:
        # Extract Category (Legendary, Non-Legendary, etc.)
        category_match = re.search(r"#(Legendary|Non_legendary|Shiny)", message_text, re.IGNORECASE)
        category = category_match.group(1).capitalize() if category_match else "Unknown Category"

        # Extract Pokémon Name
        pokemon_match = re.search(r"Pokemon Name:\s*(.+)", message_text)
        pokemon_name = pokemon_match.group(1).strip() if pokemon_match else "Unknown Pokémon"

        # Extract Level
        level_match = re.search(r"Lv\.\s*(\d+)", message_text)
        level = level_match.group(1) if level_match else "N/A"

        # Extract Nature
        nature_match = re.search(r"Nature:\s*([\w\s]+)", message_text)
        nature = nature_match.group(1).strip() if nature_match else "Unknown Nature"

        # Extract Types
        types_match = re.search(r"Types:\s*\[(.+?)\]", message_text)
        types = types_match.group(1) if types_match else "Unknown Types"

        return {
            "category": category,
            "pokemon_name": pokemon_name,
            "level": level,
            "nature": nature,
            "types": types,
        }

    return None  # If nothing matched

@bot.message_handler(commands=['nexts'])
def nexts_message(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if is_admin(message.from_user.id):
            if stored_messages:
                next_message_id = next(iter(stored_messages))
                next_message_data = stored_messages.pop(next_message_id)
                bot.forward_message(message.chat.id, next_message_data["chat_id"], next_message_id)
            else:
                bot.send_sticker(message.chat.id,OK_STICKER_ID)
                bot.reply_to(message, "<blockquote>No more Posts To Forward</blockquote>",parse_mode="html")
        else:
            bot.send_sticker(message.chat.id,ANGRY_STICKER_ID)
            bot.reply_to(message, "<blockquote>Only admins can perform this action.</blockquote>",parse_mode="html")



previous_dot_message = {}

confirmed_messages = set()  # Track confirmed sales
message_store = {}  # Store auction details
message_stor = {}

# ---- HANDLE DOT PROCESS ----
import re
import time
from telebot import types

@bot.message_handler(func=lambda message: message.text == "." and message.from_user.id in xmods)
def handle_dot(message):
    chat_id = message.chat.id
    global auce_active, poke_pros
    if auce_active == False:
        return 
    
    if poke_pros == False:
        return
    
    # Delete previous dot message if exists
    if chat_id in previous_dot_message:
        prev_msg_id = previous_dot_message[chat_id]
        if prev_msg_id not in confirmed_messages:
            try:
                bot.delete_message(chat_id, prev_msg_id)
            except Exception as e:
                print(f"Failed to delete message: {e}")

    # Animated Dots Process
    msg = bot.reply_to(message, "•")
    previous_dot_message[chat_id] = msg.message_id

    time.sleep(1.5)
    bot.edit_message_text("• •", chat_id, msg.message_id)
    time.sleep(1.5)
    bot.edit_message_text("• • •", chat_id, msg.message_id)
    time.sleep(1.5)

    # Ensure the message is a reply to a bid
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Error: Please reply to a bid message.")
        return

    bid_message = message.reply_to_message.text

    # Extract bid amount
    price_match = re.search(r"(\d+(?:\.\d+)?(?:k|pd)?)", bid_message, re.IGNORECASE)
    price = price_match.group(1) if price_match else "Unknown Price"

    # Extract buyer details
    buyer_id = message.reply_to_message.from_user.id
    fn = message.reply_to_message.from_user.full_name
    buyer_username = f"@{message.reply_to_message.from_user.username}" if message.reply_to_message.from_user.username else f'<a href="tg://user?id={buyer_id}">{fn}</a>'

    # Retrieve auction item details
    if chat_id not in message_store:
        bot.reply_to(message, "❌ No auction item found. Use `/next` first.",parse_mode='Markdown')
        return

    auction_details = message_store[chat_id]
    category = auction_details["category"]
    
    item_name = (
                auction_details.get("tm_name") or
                auction_details.get("pokemon_name") or
                auction_details.get("team_name") or
                "Unknown Item"
                )
    # Confirmation Message
    confirmation_text = f"🔹 Confirm Sale\n Item: {item_name} ({category})?"

    # Inline Button for Confirmation
    keyboard = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton(text="✅ Confirm", callback_data=f"s_{chat_id}_{msg.message_id}_{buyer_id}_{price}_{category}")
    keyboard.add(confirm_button)

    message_store[f"{chat_id}_{msg.message_id}"] = {
        "auction_details": auction_details,
        "buyer_id": buyer_id,
        "buyer_username": buyer_username,
        "price": price
    }
    print(message_store[f"{chat_id}_{msg.message_id}"])
    bot.edit_message_text(confirmation_text, chat_id, msg.message_id, reply_markup=keyboard)

# ---- HANDLE CONFIRMATION CALLBACK ----
@bot.callback_query_handler(func=lambda call: call.data.startswith("s_"))
def handle_sell_pokemon(call):
    global poke_pros,brond
    if call.from_user.id not in xmods:
        bot.answer_callback_query(call.id, text="🖕")
        return

    data = call.data.split("_")
    chat_id = int(data[1])
    message_id = int(data[2])
    buyer_id = data[3]
    price = data[4]
    category = data[5]
    confirmed_messages.add(message_id)

    sale_details = message_store.get(f"{chat_id}_{message_id}")
    if not sale_details:
        bot.answer_callback_query(call.id, "❌ Error: Sale details not found.")
        return
    
    if chat_id not in message_stor or "auction_message" not in message_stor[chat_id]:
        bot.answer_callback_query(call.id, "❌ Error: No auction item found. Use `/next` first.")
        return
    
    poke_pros = False

    forwarded_msg = message_stor[chat_id]["auction_message"]

    # Extract seller details from the forwarded message
    seller_id, seller_username = extract_seller_details(forwarded_msg)
    # Extract Pokémon/TM details using the extract_pokemon_details function
    auction_details = extract_pokemon_details(forwarded_msg)# Ensure category is correctly extracted
    category = auction_details.get("category", "Unknown Category")

    # Extract item name (Pokémon, TM, or Team)
    item_name = (
        auction_details.get("tm_name") or
        auction_details.get("pokemon_name") or
        auction_details.get("team_name") or
        "Unknown Item"
    )

# 📜 Generate full details dynamically based on category
    if category == "TMS":
        move_name = auction_details.get("move_name", "Unknown Move")
        move_type = auction_details.get("move_type", "Unknown Type")
        power = auction_details.get("power", "Unknown Power")
        accuracy = auction_details.get("accuracy", "Unknown Accuracy")

        full_details = (
            f"<blockquote>📀 TM Name: {item_name}\n"
            f"🌀 Move: {move_name} [{move_type}]\n"
            f"💥 Power: {power}|🎯 Accuracy: {accuracy}</blockquote>"
        )

    elif category in ['Legendary','Non_legendary','Shiny']:
        level = auction_details.get("level", "Unknown Level")
        nature = auction_details.get("nature", "Unknown Nature")
        types = auction_details.get("types", "Unknown Types")

        full_details = (
            f"<blockquote>🔹 Pokémon Name: {item_name}\n"
            f" Lv. {level}| Nature: {nature}\n"
            f" Types: {types}</blockquote>"
        )

    elif category == "Teams":
        team_details = auction_details.get("team_pokemon", "No team details available.")

        full_details = (
            f"<blockquote>⚔️ Team Name: {item_name}\n"
            f"📋 Team Members:\n {team_details}</blockquote>"
        )

    else:
        full_details = f"📦 **Item:** {item_name} (Category: {category})"
 
    if not auction_details:
        bot.answer_callback_query(call.id, "❌ Error: Could not extract details.")
        return

    item_name = (
            auction_details.get("tm_name") or
            auction_details.get("pokemon_name") or
            auction_details.get("team_name") or
            "Unknown Item"
        )  

    keyboard = InlineKeyboardMarkup()
    trade_button = InlineKeyboardButton(text="🔗 Trade Group", url='https://t.me/allinonehexa')
    keyboard.add(trade_button)

    # 🛒 Notify Buyer
    buyer_notification = (
        f"🎉 𝘠𝘖𝘜 𝘏𝘈𝘝𝘌 𝘚𝘜𝘊𝘊𝘌𝘚𝘚𝘍𝘜𝘓𝘓𝘠 𝘉𝘖𝘜𝘎𝘏𝘛!\n\n"
        f"➥ 𝗖𝗔𝗧𝗘𝗚𝗢𝗥𝗬 - {category}\n"
        f"➥ 𝗦𝗘𝗟𝗟𝗘𝗥 - {seller_username} (ID: <code>{seller_id}</code>)\n"
        f"➥ 𝗣𝗥𝗜𝗖𝗘 - {price}\n\n"
        f"✮ 𝙳𝙴𝚃𝙰𝙸𝙻𝚂 :\n{full_details}\n\n"
        "⚡️𝘑𝘖𝘐𝘕 𝘛𝘏𝘌 𝘛𝘙𝘈𝘋𝘌 𝘎𝘙𝘖𝘜𝘗 𝘍𝘖𝘙 𝘔𝘖𝘙𝘌 𝘋𝘌𝘈𝘓𝘚...!"
    )
    bot.send_message(buyer_id, buyer_notification, reply_markup=keyboard, parse_mode='html')

    # 🏷 Notify Seller
    seller_notification = (
        f"💰 Your {item_name} has been sold!\n\n"
        f"🎯 Buyer: {sale_details['buyer_username']} (ID: {buyer_id})\n"
        f"💰 Final Price: {price}\n\n"
        f"📜 Details:\n{full_details}\n\n"
        "✅ Please contact the buyer to finalize the trade."
    )
    bot.send_message(seller_id, seller_notification,  reply_markup=keyboard, parse_mode='html')

    # 🏆 Format Sale Message Based on Category
    category_messages = {
        "Legendary": f"🔥 A Legendary Pokémon has been sold!\n\n",
        "Non_legendary": f"⚡ A Pokémon has been sold!\n\n",
        "Shiny": f"✨ A Shiny Pokémon has been sold!\n\n",
        "TMS": f"📀 A TM Move has been sold!\n\n",
        "Teams": f"⚔️ A Team has been sold!\n\n"
    }
    category_message = category_messages.get(category, "💎 An item has been sold!\n\n")

    # Final Sale Announcement
    sell_message = (
        f"{category_message}"
        f"🎯 Sold To: {sale_details['buyer_username']} (ID: {buyer_id})\n"
        f"💰 Sold For: {price}\n\n"
        f"📜 Details:\n{full_details}\n\n"
        "📌 Join the trade group to get the seller's username after the auction."
    )
    
    # Edit Message to Show Sale Confirmation
    bot.edit_message_text(sell_message, call.message.chat.id, call.message.message_id,
                           disable_web_page_preview=True, reply_markup=keyboard, parse_mode='html')

    bot.pin_chat_message(call.message.chat.id, call.message.message_id)

    # ✅ Store the purchase details
    store_purchase(buyer_id, sale_details["buyer_username"], seller_id, seller_username, price, full_details)

    # ✅ Log Sale
    print(f"✅ {item_name} sold to {sale_details['buyer_username']} (ID: {buyer_id}) for {price}.")
    brond = True
    next_message(call.message)

buyersthings = []

import json

# File to store auction transaction data
FILE_NAME = "auctop.json"

# Dictionary to store purchase history {buyer_id: [(seller_username, seller_id, item_name, price), ...]}
purchase_history = {}

# Dictionary to store sales history {seller_id: [(buyer_username, buyer_id, item_name, price), ...]}
sales_history = {}

# Function to load data from JSON
def loa_data():
    global purchase_history, sales_history
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            purchase_history = data.get("purchase_history", {})
            sales_history = data.get("sales_history", {})
    except (FileNotFoundError, json.JSONDecodeError):
        sav_data()  # Save an empty file if not found or corrupted

# Function to save data to JSON
def sav_data():
    with open(FILE_NAME, "w") as file:
        json.dump({"purchase_history": purchase_history, "sales_history": sales_history}, file, indent=4)

# Load existing data when script starts
loa_data()

@bot.message_handler(commands=['resetall'])
def reset_all(message):
    """Clears all purchase and sales history (Admin-Only)."""
    if message.from_user.id not in xmods:
        bot.reply_to(message, "❌ You do not have permission to use this command.")
        return

    global purchase_history, sales_history  # Ensure we're modifying the global dictionaries
    purchase_history.clear()
    sales_history.clear()

    sav_data()
    bot.reply_to(message, "✅ All purchase and sales history has been **cleared** successfully!", parse_mode='markdown')

def store_purchase(buyer_id, buyer_username, seller_id, seller_username, price, details):
    """Stores purchase details for a user."""
    buyer_id = str(buyer_id)
    seller_id = str(seller_id)

    # Store for buyer
    if buyer_id not in purchase_history:
        purchase_history[buyer_id] = []
    purchase_history[buyer_id].append((seller_username, seller_id, price, details))

    # Store for seller
    if seller_id not in sales_history:
        sales_history[seller_id] = []
    sales_history[seller_id].append((buyer_username, buyer_id, price, details))
    
    buyersthings.append((buyer_id, buyer_username, seller_id, seller_username, price, details))
    sav_data()
    print(f"✅ Purchase stored: Buyer {buyer_id} from Seller {seller_id} for {price}")

@bot.message_handler(commands=['myaio'])
def myaio(message):
    """Shows the user's purchase history."""
    user_id = message.from_user.id

    if not has_started_bot(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
        bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    if not is_user_updated(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('update',url='https://t.me/Auct_he_bot?start=update'))
        bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🛒 Bought Items", callback_data=f"myaio_bought_{user_id}"),
        InlineKeyboardButton("💰 Sold Items", callback_data=f"myaio_sold_{user_id}"),
    )
    
    photo = 'https://i.postimg.cc/ncKSPcZr/AIO-AUCTION.png'
    bot.send_photo(message.chat.id, photo=photo,caption= "📜 **Select your transaction type:**", parse_mode="Markdown", reply_markup=markup, reply_to_message_id=message.message_id)


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

@bot.callback_query_handler(func=lambda call: call.data.startswith("myaio_"))
def handle_myaio_selection(call):
    """Handles inline button clicks for Bought & Sold history with pagination and proper image handling."""
    user_id = int(call.from_user.id)
    data_parts = call.data.split("_")
    
    # Ensure correct data format
    if len(data_parts) < 3:
        bot.answer_callback_query(call.id, "❌ Invalid data format.", show_alert=True)
        return

    action = data_parts[1]
    original_user_id = int(data_parts[2]) if data_parts[2].isdigit() else None
    page = int(data_parts[3]) if len(data_parts) > 3 and data_parts[3].isdigit() else 1  # Default to page 1

    # Debugging: Print extracted values
    print(f"User ID: {user_id}, Extracted Original User ID: {original_user_id}, Data Parts: {data_parts}")

    # Ensure only the user who started `/myaio` can interact
    if user_id != original_user_id:
        bot.answer_callback_query(call.id, "❌ You cannot use this button.", show_alert=True)
        return

    if action == "bought":
        history_data = purchase_history.get(str(user_id), [])
        image_url = 'https://files.catbox.moe/xmyod5.jpg'  # Bought Items Image
        title = "🛒 <b>Your Bought Items:</b>\n\n"
        switch_section_button = InlineKeyboardButton("💰 Sold Items", callback_data=f"myaio_sold_{original_user_id}_1")

    elif action == "sold":
        history_data = sales_history.get(str(user_id), [])
        image_url = 'https://i.postimg.cc/BQTqBjGf/1-a.jpg'  # Sold Items Image
        title = "💰 <b>Your Sold Items:</b>\n\n"
        switch_section_button = InlineKeyboardButton("🛒 Bought Items", callback_data=f"myaio_bought_{original_user_id}_1")

    else:
        bot.answer_callback_query(call.id, "❌ Invalid action.", show_alert=True)
        return

    # Check if history is empty
    if not history_data:
        bot.answer_callback_query(call.id, f"❌ You haven't {action} anything yet.")
        return

    # Pagination logic
    items_per_page = 6
    total_items = len(history_data)
    total_pages = (total_items + items_per_page - 1) // items_per_page  # Round up

    # Ensure page is within limits
    page = max(1, min(page, total_pages))

    # Get items for the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    history_page = history_data[start_index:end_index]

    # Format history text
    history_text = f"{title} (Page {page}/{total_pages})\n\n"
    for i, (username, userid, price, details) in enumerate(history_page, start=start_index + 1):
        history_text += (
            f"🔹 {i}. \n"
            f"   🎯 User: {username} (ID: <code>{userid}</code>)\n"
            f"   💰 Price: {price}\n\n"
            f"<blockquote>   🏛 Details:\n{details}\n\n</blockquote>"
        )

    # Inline keyboard with pagination buttons
    markup = InlineKeyboardMarkup()
    if page > 1:
        markup.add(InlineKeyboardButton("⬅ Previous", callback_data=f"myaio_{action}_{user_id}_{page-1}"))
    if page < total_pages:
        markup.add(InlineKeyboardButton("Next ➡", callback_data=f"myaio_{action}_{user_id}_{page+1}"))
    
    # Add switch section button
    markup.add(switch_section_button)
    
    sav_data()
    
    # Change image when switching sections, otherwise update text only
    if f"myaio_{action}" in call.data:
        bot.edit_message_media(
            media=InputMediaPhoto(image_url, caption=history_text, parse_mode="html"),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    else:
        bot.edit_message_text(history_text, call.message.chat.id, call.message.message_id, parse_mode="html", reply_markup=markup)
    
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

# Sample Images for Buyers & Sellers
BUYERS_IMAGE = "https://i.imghippo.com/files/Rbl9165tHM.jpg"
SELLERS_IMAGE = "https://i.postimg.cc/W3n82pQ0/1-a.jpg"

@bot.message_handler(commands=["auctop"])
def auctop(message):
    """Handles the /auctop command to show top buyers & sellers."""
    user_id = message.from_user.id
    if user_id not in xmods:
        bot.reply_to(message,"you are not authorized to use this")
        return

    # Get top buyers and sellers data
    top_buyers = get_top_buyers()
    top_sellers = get_top_sellers()

    # Generate buyer list text
    buyers_text = "🏆 <b>Top 5 Buyers</b> 🛒\n\n"
    for i, (buyer_id, username, full_name, count) in enumerate(top_buyers, start=1):
        buyers_text += (
            f"🔹 <b>{i}. {full_name}</b>\n"
            f"   🆔 <code>{buyer_id}</code>\n"
            f"   🏷 @{username if username else f'<a href="tg://user?id={user_id}">{full_name}</a>'}\n"
            f"   📦 <b>{count}</b> items bought\n\n"
        )

    # Generate seller list text
    sellers_text = "🏆 <b>Top 5 Sellers</b> 💰\n\n"
    for i, (seller_id, username, full_name, count) in enumerate(top_sellers, start=1):
        sellers_text += (
            f"🔹 <b>{i}. {full_name}</b>\n"
            f"   🆔 <code>{seller_id}</code>\n"
            f"   🏷 @{username if username else f'<a href="tg://user?id={user_id}">{full_name}</a>'}\n"
            f"   💰 <b>{count}</b> items sold\n\n"
        )

    # Inline Keyboard
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📜 Top Sellers", callback_data=f"top_sellers_{user_id}"))

    # Send initial message with top buyers
    bot.send_photo(
        chat_id=message.chat.id,
        photo=BUYERS_IMAGE,
        caption=buyers_text,
        parse_mode="html",
        reply_markup=markup,
        reply_to_message_id=message.message_id
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("top_"))
def handle_top_list(call):
    """Handles inline button clicks for switching between Top Buyers & Top Sellers."""
    user_id = int(call.from_user.id)
    data_parts = call.data.split("_")
    action = data_parts[1]
    original_user_id = int(data_parts[2])  # Extract user ID from callback data

    # Ensure only the user who started the command can interact
    if user_id != original_user_id:
        bot.answer_callback_query(call.id, "❌ You cannot use this button.", show_alert=True)
        return

    if action == "buyers":
        top_buyers = get_top_buyers()
        text = "🏆 <b>Top 5 Buyers</b> 🛒\n\n"
        for i, (buyer_id, username, full_name, count) in enumerate(top_buyers, start=1):
            text += (
                f"🔹 <b>{i}. {full_name}</b>\n"
                f"   🆔 <code>{buyer_id}</code>\n"
                f"   🏷 @{username if username else 'No Username'}\n"
                f"   📦 <b>{count}</b> items bought\n\n"
            )

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📜 Top Sellers", callback_data=f"top_sellers_{user_id}"))

        bot.edit_message_media(
            media=InputMediaPhoto(BUYERS_IMAGE, caption=text, parse_mode="HTML"),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

    elif action == "sellers":
        top_sellers = get_top_sellers()
        text = "🏆 <b>Top 5 Sellers</b> 💰\n\n"
        for i, (seller_id, username, full_name, count) in enumerate(top_sellers, start=1):
            text += (
                f"🔹 <b>{i}. {full_name}</b>\n"
                f"   🆔 <code>{seller_id}</code>\n"
                f"   🏷 @{username if username else 'No Username'}\n"
                f"   💰 <b>{count}</b> items sold\n\n"
            )

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛒 Top Buyers", callback_data=f"top_buyers_{user_id}"))

        bot.edit_message_media(
            media=InputMediaPhoto(SELLERS_IMAGE, caption=text, parse_mode="HTML"),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

def get_top_buyers():
    """Fetches the top 5 buyers from the purchase history."""
    buyer_counts = {}
    for buyer_id, purchases in purchase_history.items():
        buyer_counts[buyer_id] = len(purchases)

    sorted_buyers = sorted(buyer_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Retrieve username and full name
    return [(buyer_id, get_username(buyer_id), get_full_name(buyer_id), count) for buyer_id, count in sorted_buyers]


def get_top_sellers():
    """Fetches the top 5 sellers from the sales history."""
    seller_counts = {}
    for seller_id, sales in sales_history.items():
        seller_counts[seller_id] = len(sales)

    sorted_sellers = sorted(seller_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Retrieve username and full name
    return [(seller_id, get_username(seller_id), get_full_name(seller_id), count) for seller_id, count in sorted_sellers]


def get_username(user_id):
    """Retrieves the username of a user based on their ID."""
    try:
        user = bot.get_chat(user_id)
        return user.username if user.username else "No Username"
    except:
        return "Unknown"


def get_full_name(user_id):
    """Retrieves the full name (First & Last) of a user based on their ID."""
    try:
        user = bot.get_chat(user_id)
        return f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    except:
        return "Unknown"

@bot.message_handler(commands=["remo"])
def remove_item(message):
    if message.from_user.id not in xmods:
        bot.reply_to(message, "❌ Only admins can remove items from the auction.")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "⚠️ Usage: <code>/remo &lt;category&gt; &lt;index&gt;</code>\n"
                              "Example: <code>/remo leg 2</code>",
                     parse_mode="HTML")
        return

    category = args[1].lower()
    try:
        index = int(args[2]) - 1
    except ValueError:
        bot.reply_to(message, "⚠️ Invalid index. Please enter a number.")
        return

    category_map = {
        "leg": (legpoke_name, crat_id, vari, "legendary"),
        "nonleg": (nonleg_name, brat_id, bari, "nonleg"),
        "shiny": (shineiess, chat_id, nari, "shiny"),
        "tm": (tmen, craft_id, lari, "tmn"),
        "team": (teams, trat_id, gari, "team")
    }

    if category not in category_map:
        bot.reply_to(message, "⚠️ Invalid category! Choose from: <code>leg, nonleg, shiny, tm, team</code>", parse_mode="HTML")
        return

    name_list, link_list, hyperlink_list, user_category = category_map[category]

    if index < 0 or index >= len(name_list):
        bot.reply_to(message, "⚠️ Invalid index! No item found at that position.")
        return

    # Get item data before removal
    removed_name = name_list.pop(index)
    removed_link = link_list.pop(index)
    removed_hyperlink = hyperlink_list.pop(index)

    # Remove from users_nich by matching name + link
    for user_id, user_data in users_nich.items():
        if user_category in user_data:
            items = user_data[user_category]
            users_nich[user_id][user_category] = [
                item for item in items
                if not (item["name"] == removed_name and item["link"] == removed_link)
            ]

    save_data()
    save_users_data()

    bot.reply_to(message, f"✅ Successfully removed **{removed_name}** from auction.", parse_mode="Markdown")

    # Try deleting the original message if available
    try:
        msg_id = int(removed_link.split("/")[-1])
        bot.delete_message(log_channel, msg_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

# AUTOMATIC AUCTION CODE :-
        
@bot.message_handler(commands=['sold'])
def handle_sold(message):
    if message.from_user.id in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if message.from_user.id in admin_id:
            try:
                # Split command and arguments
                command, *args = message.text.split(' ', 1)
                if len(args) != 1:
                    raise ValueError

                # Extract Pokémon name and nature
                details = args[0].split(',')
                if len(details) != 2:
                    raise ValueError

                pokemon_name = details[0].strip()
                pokemon_nature = details[1].strip()

                # Extract the username and amount from the replied message
                username = message.reply_to_message.from_user.username
                amount = message.reply_to_message.text

                # New formatted message with the provided design
                reply_message = (
                    "🔊 𝐏𝐎𝐊𝐄𝐌𝐎𝐍 𝐒𝐎𝐋𝐃 🚀\n\n"
                    f"<blockquote>𝗣𝗼𝗸𝗲𝗺𝗼𝗻 𝗡𝗮𝗺𝗲  - \n {pokemon_name}\n\n"
                    f"𝗣𝗼𝗸𝗲𝗺𝗼𝗻 𝗡𝗮𝘁𝘂𝗿𝗲 -\n {pokemon_nature}\n\n"
                    f"🔸𝗦𝗢𝗟𝗗 𝗧𝗢 - @{username}\n"
                    f"🔸𝗦𝗢𝗟𝗗 𝗙𝗢𝗥 - {amount}</blockquote>\n\n"
                    "❗Join <a href='https://t.me/AllinoneHexa'>Trade Group</a> To Get Seller Username After Auction"
                )

                # Send the formatted reply message
                sent_message = bot.reply_to(
                    message, reply_message, parse_mode="HTML", disable_web_page_preview=True
                )
                bot.send_sticker(message.chat.id, SOLD_STICKER_ID)
                bot.pin_chat_message(message.chat.id, sent_message.id)

                # Log the sold Pokémon details
                sold_items.append((pokemon_name, pokemon_nature, username, amount))

            except ValueError:
                bot.send_sticker(message.chat.id, DOUBT_STICKER_ID)
                bot.reply_to(
                    message,
                    "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ᴛʜᴇ ғᴏʀᴍᴀᴛ : /sold ( ᴘᴏᴋᴇᴍᴏɴ ɴᴀᴍᴇ, ᴘᴏᴋᴇᴍᴏɴ ɴᴀᴛᴜʀᴇ )",
                    parse_mode="html",
                )
        else:
            bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
            bot.reply_to(
                message,
                "𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.",
                parse_mode="html",
            )

# Global list to keep track of unsold Pokémon
unsold_list = []

@bot.message_handler(commands=['unsold'])
def handle_unsold(message):
    if not auce_active:
        bot.reply_to(message, "<blockquote>𝗔𝘂𝗰𝘁𝗶𝗼𝗻 𝗜𝘀 𝗖𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗢𝗳𝗳.</blockquote>",parse_mode='html')
        return
    
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
        return

    if not is_admin(message.from_user.id):
        bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
        bot.reply_to(message, "<blockquote>𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.</blockquote>", parse_mode="html")
        return

    chat_id = message.chat.id
    if chat_id not in message_store:
        bot.send_sticker(message.chat.id, DOUBT_STICKER_ID)
        bot.reply_to(message, "<blockquote>𝙽𝚘 𝚛𝚎𝚌𝚎𝚗𝚝 𝚊𝚞𝚌𝚝𝚒𝚘𝚗 𝚏𝚘𝚞𝚗𝚍 𝚝𝚘 𝚖𝚊𝚛𝚔 𝚊𝚜 𝚞𝚗𝚜𝚘𝚕𝚍.</blockquote>", parse_mode="html")
        return

    forwarded_msg = message_stor[chat_id]["auction_message"]
    # Extract auction details
    auction_details = extract_pokemon_details(forwarded_msg)
    category = auction_details.get("category", "Unknown Category")
    item_name = auction_details.get("tm_name") or auction_details.get("pokemon_name") or auction_details.get("team_name") or "Unknown Item"
    # 📜 Generate full details dynamically based on category
    if category == "TMS":
        move_name = auction_details.get("move_name", "Unknown Move")
        move_type = auction_details.get("move_type", "Unknown Type")
        power = auction_details.get("power", "Unknown Power")
        accuracy = auction_details.get("accuracy", "Unknown Accuracy")

        full_details = (
            f"<blockquote>📀 TM Name: {item_name}\n"
            f"🌀 Move: {move_name} [{move_type}]\n"
            f"💥 Power: {power}|🎯 Accuracy: {accuracy}</blockquote>"
        )

    elif category in ['Legendary','Non_legendary','Shiny']:
        level = auction_details.get("level", "Unknown Level")
        nature = auction_details.get("nature", "Unknown Nature")
        types = auction_details.get("types", "Unknown Types")

        full_details = (
            f"<blockquote>🔹 Pokémon Name: {item_name}\n"
            f"⭐ Lv. {level}|🌿 Nature: {nature}\n"
            f"⚡ Types: {types}</blockquote>"
        )

    elif category == "Teams":
        team_details = auction_details.get("team_pokemon", "No team details available.")

        full_details = (
            f"<blockquote>⚔️ Team Name: {item_name}\n"
            f"📋 Team Members:\n {team_details}</blockquote>"
        )

    else:
        full_details = f"📦 **Item:** {item_name} (Category: {category})"
 

    # Extract seller details
    seller_id, seller_username = extract_seller_details(message_stor[chat_id]["auction_message"])

    # Send the unsold message in the auction chat
    reply_message = (
        f"<blockquote>❌ {item_name} Has Been Marked as Unsold</blockquote>\n\n"
        f"📜 <b>Details:</b>\n{full_details}"
    )
    sent_message = bot.reply_to(message, reply_message, parse_mode="html")

    # Send sticker and pin message
    bot.send_sticker(message.chat.id, SAD_STICKER_ID)
    bot.pin_chat_message(message.chat.id, sent_message.id)

    keyboard = InlineKeyboardMarkup()
    trade_button = InlineKeyboardButton(text="🔗 Trade Group", url='https://t.me/allinonehexa')
    keyboard.add(trade_button)
    
    # 🏷 Notify Seller
    seller_notification = (
        f"⚠️ <b>Your item was not sold!</b>\n\n"
        f"📦 <b>Item:</b> {item_name}\n"
        f"📜 <b>Category:</b> {category}\n"
        f"💔 <b>It has been marked as unsold.</b>\n\n"
        f"📋 <b>Details:</b>\n{full_details}\n\n"
        "✅ You can try auctioning it again!"
    )
    bot.send_sticker(seller_id, SAD_STICKER_ID)
    bot.send_message(seller_id, seller_notification, parse_mode="html", reply_markup=keyboard)

    print(f"🚨 {item_name} was marked as UNSOLD. Seller: {seller_username} (ID: {seller_id})")

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

ADMIN_GROUP_ID = -1002173824142  # Replace with your admin group ID
user_cache = {}  # Stores user reports temporarily

@bot.message_handler(commands=['help'])
def help_command(message):
    
    user_id = message.from_user.id
    if not has_started_bot(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
        bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    if not is_user_updated(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('update',url='https://t.me/Auct_he_bot?start=update'))
        bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    """Handles the /help command and sends inline buttons."""
    if message.chat.type != "private":  # Ensure it only works in DM
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('help',url='https://t.me/Auct_he_bot?start=help'))
        bot.reply_to(message, "❌ This command only works in my DM.",reply_markup=markup, disable_web_page_preview=True)
        return

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📸 Report an Error", callback_data="help_error"),
        InlineKeyboardButton("🚫 Request a Ban", callback_data="help_ban"),
        InlineKeyboardButton("🛑 Report Bad Words", callback_data="help_badwords"),
        InlineKeyboardButton("❓ Other Issues", callback_data="help_other"),
        InlineKeyboardButton("💻 Commands", callback_data="help_command")
    )

    bot.send_message(message.chat.id, "<b>🤖 𝘏𝘰𝘸 𝘊𝘢𝘯 𝘐 𝘏𝘦𝘭𝘱 𝘠𝘰𝘶?</b>\n\n𝘚𝘦𝘭𝘦𝘤𝘵 𝘈𝘯 𝘖𝘱𝘵𝘪𝘰𝘯 𝘉𝘦𝘭𝘰𝘸 :", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "help_command")
def handle_help_back(call):
    text = (
        "<blockquote><b>Here is the commands that users can use.\n </b>"
            "<code>/start</code> -  to start the bot\n"
            "<code>/help</code> - to help in the things of bot or group.\n"
            "<code>/add</code> - To add any items in our auction.\n"
            "<code>/profile</code> - To view your status in our auction.\n"
            "<code>/rules</code> - to check the rules\n"
            "<code>/apin</code> - to pin hexa bot messages.\n"
            "<code>/elements</code> -  to check the items in the current auction.\n"
            "<code>/myaio</code> -  to check what all you bought or sold in our auction.\n"
            "<code>/natures</code> - To check the natures list\n"
            "<code>/tm00</code> - To get tms list and particular tm too.</blockquote>"
            )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode='html'
    )

@bot.callback_query_handler(func=lambda call: call.data == "help_error")
def ask_error_photo(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>OK</b>",
        parse_mode='html'
    )
    bot.send_message(call.message.chat.id, "📸 **Send a screenshot of the error.**",parse_mode='markdown')
    bot.register_next_step_handler(call.message, receive_error_photo)

def receive_error_photo(message):
    """Receives an error photo and asks for error type."""
    if not message.photo:
        bot.send_message(message.chat.id, "❌ Please send a photo of the error.")
        return

    user_cache[message.chat.id] = {"error_photo": message.photo[-1].file_id}

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("⚙️ Bot Issue", callback_data="error_bot"),
        InlineKeyboardButton("🌐 Network Issue", callback_data="error_network"),
        InlineKeyboardButton("📄 Other", callback_data="error_other")
    )

    bot.send_message(message.chat.id, "📌 **Select the type of error:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("error_"))
def forward_error_report(call):
    """Forwards error details to the admin group."""
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>OK</b>",
        parse_mode='html'
    )
    error_type = call.data.split("_")[1]
    user_id = call.message.chat.id
    user_info = f"🆔 User ID: `{user_id}`\n👤 Username: @{call.from_user.username or 'No Username'}"

    error_photo = user_cache.get(user_id, {}).get("error_photo")

    caption = f"🚨 Error Reported! 🚨\n\n🔹 Type: {error_type.capitalize()}\n{user_info} \n@benzenez\n@smit_2446\n@Orochimaruu5828"

    bot.send_photo(ADMIN_GROUP_ID, error_photo, caption=caption)
    bot.send_message(user_id, "✅ **Your error report has been forwarded to the admins!**",parse_mode='markdown')

@bot.callback_query_handler(func=lambda call: call.data == "help_ban")
def ask_ban_photos(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>OK</b>",
        parse_mode='html'
    )
    bot.send_message(call.message.chat.id, "📸 **Send proof (photos/videos) of the scammer.** You can send multiple.",parse_mode='markdown')
    bot.register_next_step_handler(call.message, receive_ban_photos)

def receive_ban_photos(message):
    """Receives scam proof and asks for scammer's details."""
    if not message.photo:
        bot.send_message(message.chat.id, "❌ Please send at least one photo/video as proof.")
        return

    user_cache[message.chat.id] = {"ban_photos": [message.photo[-1].file_id]}

    bot.send_message(message.chat.id, "🔹 **Enter the scammer's username and ID (if available).**",parse_mode='markdown')
    bot.register_next_step_handler(message, forward_ban_request)

def forward_ban_request(message):
    """Forwards ban request to the admin group."""
    scammer_info = message.text
    user_id = message.chat.id
    user_info = f"🆔 User ID: `{user_id}`\n👤 Username: @{message.from_user.username or 'No Username'}"

    caption = f"🚨 **Ban Request!** 🚨\n\n🔹 **Scammer Info:** {scammer_info}\n{user_info} \n@benzenez\n@smit_2446\n@Orochimaruu5828"

    ban_photos = user_cache.get(user_id, {}).get("ban_photos", [])
    media = [InputMediaPhoto(photo) for photo in ban_photos]

    if media:
        bot.send_media_group(ADMIN_GROUP_ID, media)

    bot.send_message(ADMIN_GROUP_ID, caption)
    bot.send_message(user_id, "✅ **Your ban request has been sent to the admins!**",parse_mode='markdown')

@bot.callback_query_handler(func=lambda call: call.data == "help_badwords")
def ask_badword_details(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>OK</b>",
        parse_mode='html'
    )
    bot.send_message(call.message.chat.id, "🚨 **Who used the bad words?**\nEnter their username and ID.",parse_mode='markdown')
    bot.register_next_step_handler(call.message, receive_badword_details)

def receive_badword_details(message):
    user_cache[message.chat.id] = {"badword_user": message.text}

    bot.send_message(message.chat.id, "📌 **Forward the message containing bad words.**",parse_mode='markdown')
    bot.register_next_step_handler(message, forward_badword_report)

def forward_badword_report(message):
    """Forwards bad words report to the admin group."""
    if not message.forward_date:
        bot.send_message(message.chat.id, "❌ You must forward the message containing bad words.")
        return

    badword_user = user_cache.get(message.chat.id, {}).get("badword_user", "Unknown")
    user_info = f"🆔 User ID: `{message.chat.id}`\n👤 Username: @{message.from_user.username or 'No Username'}"

    caption = f"🚨 Bad Words Report! 🚨\n\n🔹 Reported User: {badword_user}\n{user_info} \n@benzenez\n@smit_2446\n@Orochimaruu5828"

    bot.forward_message(ADMIN_GROUP_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_GROUP_ID, caption)
    bot.send_message(message.chat.id, "✅ **Your report has been sent to the admins!**",parse_mode='markdown')

@bot.callback_query_handler(func=lambda call: call.data == "help_other")
def ask_other_issue(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>OK</b>",
        parse_mode='html'
    )
    bot.send_message(call.message.chat.id, "💬 **Describe your issue briefly.**",parse_mode='markdown')
    bot.register_next_step_handler(call.message, forward_other_issue)

def forward_other_issue(message):
    user_info = f"🆔 User ID: `{message.chat.id}`\n👤 Username: @{message.from_user.username or 'No Username'}"
    issue_text = message.text

    caption = f"🚨 **User Needs Help!** 🚨\n\n🔹 **Issue:** {issue_text}\n{user_info} \n@benzenez\n@smit_2446\n@Orochimaruu5828"

    bot.send_message(ADMIN_GROUP_ID, caption, parse_mode="markdown")
    bot.send_message(message.chat.id, "✅ **Your request has been forwarded to the admins!**")


@bot.message_handler(commands=['list_unsold'])
def list_unsold(message):
    if is_admin(message.from_user.id):
        if unsold_list:
            # Create a formatted list of unsold Pokémon
            unsold_message = "\n".join([f"• {pokemon}" for pokemon in unsold_list])
            reply_message = f"<b>📋 Unsold Pokémon List:</b>\n{unsold_message}"
        else:
            # Handle empty list
            reply_message = "<b>No Pokémon are currently marked as unsold.</b>"
        bot.reply_to(message, reply_message, parse_mode="html")
    else:
        # Handle unauthorized users
        bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
        bot.reply_to(message, "<blockquote>𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.</blockquote>", parse_mode="html")



@bot.message_handler(commands=['remove_unsold'])
def remove_unsold(message):
    if is_admin(message.from_user.id):
        try:
            # Extract Pokémon name from the message
            pokemon_name = message.text.split(' ', 1)[1].strip()

            # Check if the Pokémon exists in the unsold list
            if pokemon_name in unsold_list:
                unsold_list.remove(pokemon_name)  # Remove the Pokémon
                reply_message = f"<blockquote>✅ {pokemon_name} Has Been Removed From the Unsold List</blockquote>"
                bot.reply_to(message, reply_message, parse_mode="html")
            else:
                # Handle Pokémon not found in the list
                bot.send_sticker(message.chat.id, DOUBT_STICKER_ID)
                bot.reply_to(
                    message,
                    f"<blockquote>❌ {pokemon_name} Is Not in the Unsold List</blockquote>",
                    parse_mode="html",
                )
        except IndexError:
            # Handle missing Pokémon name
            bot.send_sticker(message.chat.id, DOUBT_STICKER_ID)
            bot.reply_to(
                message,
                "<blockquote>𝙿𝚕𝚎𝚊𝚜𝚎 𝚙𝚛𝚘𝚟𝚒𝚍𝚎 𝚝𝚑𝚎 𝚗𝚊𝚖𝚎 𝚘𝚏 𝚝𝚑𝚎 𝙿𝚘𝚔é𝚖𝚘𝚗 𝚝𝚘 𝚛𝚎𝚖𝚘𝚟𝚎 𝚏𝚛𝚘𝚖 𝚝𝚑𝚎 𝚞𝚗𝚜𝚘𝚕𝚍 𝚕𝚒𝚜𝚝.</blockquote>",
                parse_mode="html",
            )
    else:
        # Handle unauthorized users
        bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
        bot.reply_to(
            message,
            "<blockquote>𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.</blockquote>",
            parse_mode="html",
        )

@bot.message_handler(commands=['lock'])
def lock_all_users(message):
    chat_id = message.chat.id

    # Check if the sender is an admin
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ You must be an admin to use this command.")
        return

    try:
        # Restrict all non-admin users
        bot.set_chat_permissions(
            chat_id,
            permissions=types.ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )

        bot.reply_to(message, "🔒 **All users have been locked!** They can no longer send messages or media.", parse_mode='markdown')

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")
        
@bot.message_handler(commands=['unlock'])
def lock_all_users(message):
    chat_id = message.chat.id

    # Check if the sender is an admin
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ You must be an admin to use this command.")
        return

    try:
        # Restrict all non-admin users
        bot.set_chat_permissions(
            chat_id,
            permissions=types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )
        
        bot.reply_to(message, "🔒 **All users have been unlocked!** They can send messages only", parse_mode='markdown')

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

@bot.message_handler(commands=['reset_unsold'])
def reset_unsold(message):
    if is_admin(message.from_user.id):
        if unsold_list:
            # Clear the unsold list
            unsold_list.clear()
            reply_message = "<blockquote>✅ The Unsold List Has Been Successfully Reset</blockquote>"
            bot.reply_to(message, reply_message, parse_mode="html")
        else:
            # Handle already empty list
            bot.send_sticker(message.chat.id, DOUBT_STICKER_ID)
            bot.reply_to(
                message,
                "<blockquote>⚠️ The Unsold List Is Already Empty</blockquote>",
                parse_mode="html",
            )
    else:
        # Handle unauthorized users
        bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
        bot.reply_to(
            message,
            "<blockquote>𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.</blockquote>",
            parse_mode="html",
        )

# Dictionary to keep track of users waiting for input
waiting_for_pokemon_name = {}

@bot.message_handler(commands=['add_unsold'])
def add_unsold_command(message):
    if is_admin(message.from_user.id):
        # Prompt the user to enter the Pokémon name
        bot.reply_to(
            message,
            "<blockquote>ℹ️ Please enter the Pokémon name to add to the Unsold List:</blockquote>",
            parse_mode="html",
        )
        # Mark the user as waiting for a Pokémon name
        waiting_for_pokemon_name[message.from_user.id] = True
    else:
        # Handle unauthorized users
        bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
        bot.reply_to(
            message,
            "<blockquote>𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.</blockquote>",
            parse_mode="html",
        )

@bot.message_handler(func=lambda message: message.from_user.id in waiting_for_pokemon_name)
def handle_pokemon_name_input(message):
    # Remove the user from the waiting list
    del waiting_for_pokemon_name[message.from_user.id]

    pokemon_name = message.text.strip()

    if pokemon_name:
        # Add the Pokémon to the unsold list
        unsold_list.append(pokemon_name)
        reply_message = f"<blockquote>✅ {pokemon_name} Has Been Added to the Unsold List</blockquote>"
        bot.reply_to(message, reply_message, parse_mode="html")
    else:
        # Handle empty input
        bot.send_sticker(message.chat.id, DOUBT_STICKER_ID)
        bot.reply_to(
            message,
            "<blockquote>❌ Invalid Pokémon name. Please try again with a valid name.</blockquote>",
            parse_mode="html",
        )

# Replace this with the username of the bot whose messages should be pinned (without the '@')
TARGET_BOT_USERNAME = ["hexamonbot" , "auct_he_bot"]  # Replace with the actual bot username (e.g., "MyTargetBot")

# Handle /apin command to show timing buttons for pinning a replied message
@bot.message_handler(commands=["apin"])
def handle_apin_command(message):
    """
    Displays inline timing buttons for pinning the replied message if it is from the specified bot.
    """
    user_id = message.from_user.id
    
    if not has_started_bot(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
        bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    if not is_user_updated(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('update',url='https://t.me/Auct_he_bot?start=update'))
        bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    try:
        chat_id = message.chat.id

        # Check if the message is a reply
        if message.reply_to_message:
            replied_from_user = message.reply_to_message.from_user
            if replied_from_user:
                print(f"Replied message is from: {replied_from_user.username}, is_bot: {replied_from_user.is_bot}")  # Debugging log

                # Check if the replied message is from the target bot
                if (
                    replied_from_user.is_bot and 
                    replied_from_user.username and 
                    replied_from_user.username.lower() in TARGET_BOT_USERNAME
                ):
                    reply_message_id = message.reply_to_message.message_id
                    
                    markup = InlineKeyboardMarkup(row_width=2)  # 2 buttons per row

                    buttons = []
                    for minutes in [1, 3, 5, 10, 12, 15, 17, 20]:
                        buttons.append(InlineKeyboardButton(f"{minutes}m", callback_data=f"pin_{reply_message_id}_{minutes}"))

                    # Add buttons to markup in rows of 2
                    for i in range(0, len(buttons), 4):
                        markup.row(*buttons[i:i+4])  # Add two buttons per row

                    bot.send_message(chat_id, "⏱ Select the time for how long the message should be pinned:", reply_markup=markup)

                else:
                    bot.reply_to(
                        message,
                        f"This message is not from the target bot @{TARGET_BOT_USERNAME}."
                    )
            else:
                bot.reply_to(message, "Could not determine the sender of the replied message.")
        else:
            bot.reply_to(message, "Please reply to a message to use /apin.")

    except Exception as e:
        print(f"Error in /apin command: {e}")
        bot.reply_to(message, "An error occurred while processing your /apin command.")

# Handle button clicks for pinning and setting unpin timers
@bot.callback_query_handler(func=lambda call: call.data.startswith("pin_"))
def handle_pin_with_timer(call):
    """
    Pins a message after the user selects a timing and sets a timer for unpinning.
    """
    try:
        data = call.data.split("_")  # Extract details from callback data
        message_id = int(data[1])  # Replied message ID
        pin_time = int(data[2])  # Selected time in minutes
        chat_id = call.message.chat.id

        # Pin the message
        bot.pin_chat_message(chat_id, message_id)

        # Edit the original inline buttons message to confirm the action
        bot.edit_message_text(
            f"📌 The message has been pinned for {pin_time} minutes.",
            chat_id=chat_id,
            message_id=call.message.message_id
        )

        # Notify the user with a short confirmation
        bot.answer_callback_query(call.id, f"📌 Message pinned for {pin_time} minutes.")

        # Start a timer thread for unpinning
        threading.Thread(target=unpin_message_after_delay, args=(chat_id, message_id, pin_time)).start()

    except Exception as e:
        print(f"Error in handle_pin_with_timer: {e}")
        bot.answer_callback_query(call.id, "An error occurred while processing your request.")

def unpin_message_after_delay(chat_id, message_id, delay_minutes):
    """
    Waits for the specified time and then unpins the message.
    """
    try:
        time.sleep(delay_minutes * 60)  # Convert minutes to seconds
        bot.unpin_chat_message(chat_id, message_id)
        bot.send_message(chat_id, f"🚫 The pinned message has been unpinned after {delay_minutes} minutes.")
    except Exception as e:
        print(f"Error in unpin_message_after_delay: {e}")


# Assuming sold_items is defined as a global list
sold_items = []

@bot.message_handler(commands=['buyers'])
def handle_buyers(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if message.from_user.id not in admin_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        if not sold_items:
            bot.reply_to(message, "No items have been sold yet.")
            return

        buyers_list = "📋 List of Buyers:\n\n"
        for pokemon_name, pokemon_nature, buyer_username, amount  in sold_items:
            buyers_list += f"🔹{pokemon_name} ({pokemon_nature}) sold to @{buyer_username} for {amount}\n"

        bot.reply_to(message, buyers_list)

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ Number of items per page
ITEMS_PER_PAGE = 6

# ✅ Pagination cache to store the page index per user
user_page_cache = {}

@bot.message_handler(commands=['details'])
def handle_buyers(message):
    user_id = message.from_user.id
    if str(user_id) in banned_users:
        bot.reply_to(message, "❌ You are banned by an administrator.")
        return
    
    if user_id not in admin_id:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return
    
    if not buyersthings:
        bot.reply_to(message, "ℹ️ No items have been sold yet.")
        return

    # ✅ Initialize user page to 0 if not set
    user_page_cache[user_id] = 0
    send_buyer_list(message, page=0)

def send_buyer_list(message, page=0):
    user_id = message.from_user.id
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    buyers_list = "📋 <b>List of Buyers:</b>\n\n"
    paged_items = buyersthings[start_index:end_index]

    if not paged_items:
        buyers_list = "❌ No items found on this page."
    else:
        for buyer_id, buyer_username, seller_id, seller_username, price, details in paged_items:
            buyers_list += (
                f"🔹 <b>Buyer ID:</b> <code>{buyer_id}</code>\n"
                f"👤 <b>Username:</b> @{buyer_username}\n"
                f"🛍️ <b>Seller ID:</b> <code>{seller_id}</code>\n"
                f"👤 <b>Username:</b> @{seller_username}\n"
                f"💰 <b>Bought Price:</b> {price}\n"
                f"📄 <b>Details:</b> {details}\n\n"
            )
    
    # ✅ Create inline keyboard for pagination
    markup = InlineKeyboardMarkup()
    buttons = []

    if page > 0:
        buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"buyers_prev_{page-1}"))

    if end_index < len(buyersthings):
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"buyers_next_{page+1}"))

    markup.row(*buttons)

    # ✅ Send the message with pagination
    if message.chat.type == "private":
        bot.send_message(
            user_id, buyers_list, parse_mode='html', reply_markup=markup, disable_web_page_preview=True
        )
    else:
        bot.reply_to(
            message, buyers_list, parse_mode='html', reply_markup=markup, disable_web_page_preview=True
        )

# ✅ Callback handler for pagination
@bot.callback_query_handler(func=lambda call: call.data.startswith('buyers_'))
def handle_buyer_pagination(call):
    user_id = call.from_user.id
    if user_id not in admin_id:
        bot.answer_callback_query(call.id, "❌ You are not authorized to navigate this list.")
        return
    
    # ✅ Parse the callback data
    action, direction, page_str = call.data.split('_')
    page = int(page_str)
    
    # ✅ Update the current page for the user
    user_page_cache[user_id] = page

    # ✅ Edit the original message with the new page content
    try:
        send_buyer_list(call.message, page=page)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error handling pagination: {e}")

@bot.message_handler(commands=['reset_buyers'])
def reset_buyers(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if message.from_user.id not in admin_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        global sold_items
        sold_items.clear()  # Clear the buyers list
        bot.reply_to(message, "The buyers list has been reset.")

# Command to remove a buyer from the list
@bot.message_handler(commands=['remove_buyer'])
def remove_buyer(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
        return

    if message.from_user.id not in admin_id:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    # Check if the command contains a username to remove
    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.reply_to(message, "Please specify the username of the buyer to remove. Example: /remove_buyer username")
        return

    buyer_username = command_parts[1]  # Extract the username
    global sold_items
    updated_sold_items = [item for item in sold_items if item[2] != buyer_username]  # Remove buyer by username

    if len(sold_items) == len(updated_sold_items):
        bot.reply_to(message, f"No buyer found with username @{buyer_username}.")
    else:
        sold_items = updated_sold_items
        bot.reply_to(message, f"Buyer @{buyer_username} has been removed from the list.")


# Command to add a buyer to the list
@bot.message_handler(commands=['add_buyer'])
def add_buyer(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
        return

    if message.from_user.id not in admin_id:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    # Check if the command contains all required details
    command_parts = message.text.split(maxsplit=4)
    if len(command_parts) < 5:
        bot.reply_to(
            message,
            "Please provide all the required details in the format:\n"
            "/add_buyer Pokémon_Name Pokémon_Nature Buyer_Username Amount\n"
            "Example: /add_buyer Pikachu Jolly john_doe 500"
        )
        return

    # Extract details from the command
    pokemon_name = command_parts[1]
    pokemon_nature = command_parts[2]
    buyer_username = command_parts[3].strip('@')  # Remove "@" if provided
    amount = command_parts[4]

    # Add the buyer to the list
    global sold_items
    sold_items.append((pokemon_name, pokemon_nature, buyer_username, amount))
    bot.reply_to(
        message,
        f"Buyer @{buyer_username} has been added to the list:\n"
        f"🔹 {pokemon_name} ({pokemon_nature}) sold for {amount}."
    )
    
# Define broadcast lists
broad_users = []  # List of private chat user IDs
broad_groups = []  # List of group chat IDs

# Define admin list
admin_ids_broad = ["1952192480", "1897434080", "6210317431", "5750189157",]  # Replace with actual admin user IDs
banned_users = []  # List of banned user IDs

from telebot.types import Message
import html

@bot.message_handler(commands=["abroad"])
def broadcast(message: Message):
    if message.from_user.id not in xmods:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    sent_count = 0
    failed_count = 0
    recipient_list = []

    def format_user_link(user_id, name):
        """Properly format and escape user links to avoid errors."""
        safe_name = html.escape(name)   
        return f" <a href='tg://user?id={user_id}'>{safe_name}</a>"
    
    # If the command is replying to a message, forward it
    if message.reply_to_message:
        for user_id, user_data in users.items():
            try:
                bot.forward_message(user_id, message.chat.id, message.reply_to_message.message_id)
                name = user_data.get('name','unknown')
                sent_count += 1
                recipient_list.append(f"👤 {format_user_link(user_id,name)} ({user_data.get('username', 'NoUsername')}) - <code>{user_id}</code>")
            except Exception as e:
                failed_count += 1
                print(f"Could not send to {user_id}: {e}")

        bot.reply_to(message, f"✅ Broadcast forwarded to **{sent_count}** users. ({failed_count} failed)",parse_mode='Markdown')

    # If the command is used with text, send that text
    elif len(message.text.split()) > 1:
        text = message.text.replace("/abroad ", "")
        for user_id, user_data in users.items():
            try:
                bot.send_message(user_id, f"📢 <b>Broadcast Message:</b>\n\n{text}", parse_mode="html")
                name = user_data.get('name','unknown')
                sent_count += 1
                recipient_list.append(f"👤 {format_user_link(user_id,name)} ({user_data.get('username', 'NoUsername')}) - <code>{user_id}</code>")
            except Exception as e:
                failed_count += 1
                print(f"Could not send to {user_id}: {e}")

        bot.reply_to(message, f"✅ Broadcast sent to <b>{sent_count}</b> users. ({failed_count} failed)",parse_mode='html')

    else:
        bot.reply_to(message, "❌ Please reply to a message or type a message to send.")
        return

    # Send recipient list in the group
    if recipient_list:
        recipient_text = "📋 <b>Broadcast Recipients:</b>\n\n" + "\n".join(recipient_list)
        bot.send_message(-1002173824142, recipient_text, parse_mode="HTML")

# Dynamic list management for users and groups
@bot.message_handler(commands=['add_user', 'remove_user', 'add_group', 'remove_group'])
def manage_broadcast_list(message):
    user_id = message.chat.id
    if str(user_id) in admin_ids_broad:
        try:
            command, target_id = message.text.split(maxsplit=1)

            if command == '/add_user':
                if target_id not in broad_users:
                    broad_users.append(target_id)
                    bot.reply_to(message, f"<blockquote>User {target_id} added to the broadcast list.</blockquote>", parse_mode="html")
                else:
                    bot.reply_to(message, f"<blockquote>User {target_id} is already in the list.</blockquote>", parse_mode="html")

            elif command == '/remove_user':
                if target_id in broad_users:
                    broad_users.remove(target_id)
                    bot.reply_to(message, f"<blockquote>User {target_id} removed from the broadcast list.</blockquote>", parse_mode="html")
                else:
                    bot.reply_to(message, f"<blockquote>User {target_id} is not in the list.</blockquote>", parse_mode="html")

            elif command == '/add_group':
                if target_id not in broad_groups:
                    broad_groups.append(target_id)
                    bot.reply_to(message, f"<blockquote>Group {target_id} added to the broadcast list.</blockquote>", parse_mode="html")
                else:
                    bot.reply_to(message, f"<blockquote>Group {target_id} is already in the list.</blockquote>", parse_mode="html")

            elif command == '/remove_group':
                if target_id in broad_groups:
                    broad_groups.remove(target_id)
                    bot.reply_to(message, f"<blockquote>Group {target_id} removed from the broadcast list.</blockquote>", parse_mode="html")
                else:
                    bot.reply_to(message, f"<blockquote>Group {target_id} is not in the list.</blockquote>", parse_mode="html")

        except ValueError:
            bot.reply_to(message, "<blockquote>Please provide a valid target ID.</blockquote>", parse_mode="html")
    else:
        bot.reply_to(message, "<blockquote>You are not authorized to manage the broadcast list.</blockquote>", parse_mode="html")

group_id = -1002022693265

@bot.message_handler(commands=['forward'])
def send_message_prompt(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if is_admin(message.from_user.id):
            bot.reply_to(message, "<blockquote>Type the message to send in the group</blockquote>",parse_mode="html")
            bot.register_next_step_handler(message, send_message)
        else:
            bot.send_sticker(message.chat.id,ANGRY_STICKER_ID)
            bot.reply_to(message, "<blockquote>𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.</blockquote>",parse_mode="html")

def send_message(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if message.forward_from or message.forward_from_chat:
            forwarded_message = message
        else:
            forwarded_message = message.text
        try:
            bot.forward_message(group_id, message.chat.id, message.id)
            bot.send_message(message.chat.id, "<blockquote>Message sent successfully.</blockquote>",parse_mode="html")
        except Exception as e:
            bot.send_message(message.chat.id, f"Failed to send message: {e}")

@bot.message_handler(commands=['users'])
def handle_users(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        user_id = message.from_user.id
        if str(user_id) in str(admin_id):
            num_users = len(started_users)
            bot.send_message(message.chat.id, f"Total users : {num_users}")
        else:
            bot.send_sticker(message.chat.id,ANGRY_STICKER_ID)
            bot.send_message(message.chat.id, "<blockquote>𝚈𝚘𝚞 𝚊𝚛𝚎 𝚗𝚘𝚝 𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍 𝚝𝚘 𝚞𝚜𝚎 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍.</blockquote>",parse_mode="html")

admin_ids = ['1897434080', '5750189157', '1896198661', '6969086416', '1952192480']  # Updated admin list


# Function to get username or user ID for display
def get_username_or_id(user_id):
    try:
        user = bot.get_chat(user_id)
        if user.username:
            return f'@{user.username}'
        else:
            return f'{user.id}'  # Fallback to user ID if no username
    except telebot.apihelper.ApiTelegramException:
        return f'{user_id} (unable to fetch details)'

# Command to validate username format
def is_valid_username(username):
    # Regex to ensure valid Telegram username: starts with letter/number, and only letters, numbers, and underscores
    return re.match(r'^[a-zA-Z0-9_]{5,32}$', username) is not None

# Escape Markdown special characters
def escape_markdown(text):
    # List of special characters in Markdown
    special_characters = ['\\', '*', '_', '{', '}', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '.', '!']

    # Escape special characters
    for char in special_characters:
        text = text.replace(char, f'\\{char}')

    return text

# Admin command to promote a user to admin using username or ID
@bot.message_handler(commands=['admin'])
def add_admin(message):
    # Check if the user sending the command is an admin
    if str(message.from_user.id) not in admin_ids:
        bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
        bot.send_message(
            message.chat.id,
            "<blockquote>Only current admins can use this command.</blockquote>",
            parse_mode="html"
        )
        return

    try:
        # Split the message to get the identifier (username or user_id)
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            bot.send_message(
                message.chat.id,
                "<blockquote>Usage: /admin <@username or user_id></blockquote>",
                parse_mode="html"
            )
            return

        identifier = args[1].strip()  # Capture the username or user ID

        # Handle username or user ID
        if identifier.startswith('@'):  # If a username is provided
            username = identifier[1:]  # Remove the '@'
            if not is_valid_username(username):
                bot.send_message(message.chat.id, "Invalid username format.")
                return
            try:
                user = bot.get_chat(username)  # Fetch user globally
                user_id = user.id
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(message.chat.id, f"User @{username} not found.")
                return
        else:  # If an ID is provided
            try:
                user_id = int(identifier)
            except ValueError:
                bot.send_message(message.chat.id, "Invalid user ID.")
                return

        # Add the user to the admin list if not already an admin
        if str(user_id) not in admin_ids:
            admin_ids.append(str(user_id))  # Store as string
            bot.send_message(
                message.chat.id,
                f"User {get_username_or_id(user_id)} has been added to the admin list."
            )
        else:
            bot.send_message(
                message.chat.id,
                f"User {get_username_or_id(user_id)} is already an admin."
            )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"An error occurred while processing the request: {str(e)}"
        )


# Command to list all admins
@bot.message_handler(commands=['admins'])
def handle_admins(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
        return

    response = "Bot Administrators:\n\n"
    for admin_id in admin_ids:
        username = get_username_or_id(admin_id)
        response += f"• {escape_markdown(username)} ✨\n"  # Escape Markdown characters in usernames

    bot.reply_to(message, response, parse_mode='Markdown')

# Command to handle banned users
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if str(message.from_user.id) not in admin_ids:
        bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
        bot.send_message(
            message.chat.id,
            "<blockquote>Only current admins can use this command.</blockquote>",
            parse_mode="html"
        )
        return

    try:
        # Split the message to get the identifier (username or user_id)
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            bot.send_message(
                message.chat.id,
                "<blockquote>Usage: /ban <@username or user_id></blockquote>",
                parse_mode="html"
            )
            return

        identifier = args[1].strip()  # Capture the username or user ID

        # Handle username or user ID
        if identifier.startswith('@'):  # If a username is provided
            username = identifier[1:]  # Remove the '@'
            if not is_valid_username(username):
                bot.send_message(message.chat.id, "Invalid username format.")
                return
            try:
                user = bot.get_chat(username)  # Fetch user globally
                user_id = user.id
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(message.chat.id, f"User @{username} not found.")
                return
        else:  # If an ID is provided
            try:
                user_id = int(identifier)
            except ValueError:
                bot.send_message(message.chat.id, "Invalid user ID.")
                return

        # Add user to banned list
        if str(user_id) not in banned_users:
            banned_users.append(str(user_id))
            bot.send_message(
                message.chat.id,
                f"User {get_username_or_id(user_id)} has been banned."
            )
        else:
            bot.send_message(
                message.chat.id,
                f"User {get_username_or_id(user_id)} is already banned."
            )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"An error occurred while processing the request: {str(e)}"
        )

def escape_markdown(text):
    """
    Escape special characters for Telegram MarkdownV2.
    """
    if not text:
        return ""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', str(text))



import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO

# Public URLs to profile templates
TEMPLATES = {
    1: "https://i.postimg.cc/9FWJBGr8/photo-2025-02-03-17-25-42.jpg",
    2: "https://i.postimg.cc/rwHjc3g3/photo-2025-02-03-17-30-24.jpg",
    3: "https://i.postimg.cc/KjmrJ2vk/photo-2025-02-03-17-33-32.jpg",
    4: "https://i.postimg.cc/sxKPLNvn/photo-2025-02-03-17-51-49.jpg",
    5: "https://i.postimg.cc/7LTVL9W6/photo-2025-02-03-17-54-38.jpg",
    6: "https://i.postimg.cc/gkkHhmT1/photo-2025-02-03-18-39-00.jpg",
    7: "https://i.postimg.cc/sgbYbSgR/photo-2025-02-03-18-39-01.jpg",
    8: "https://i.postimg.cc/VsFF5dDj/photo-2025-02-03-18-39-01-2.jpg",
    9: "https://i.postimg.cc/K8179QFN/photo-2025-02-03-18-39-01-3.jpg",
    10: "https://i.postimg.cc/tTjh4j6S/photo-2025-02-03-18-39-01-4.jpg",
    11: "https://i.postimg.cc/RhPfdJDy/photo-2025-02-03-18-39-02.jpg",
    12: "https://i.postimg.cc/xC3Lk4y0/photo-2025-02-03-18-39-02-2.jpg",
    13: "https://i.postimg.cc/RhCKwLXw/photo-2025-02-03-18-39-02-3.jpg"
}

# Dictionary to store user-selected templates
user_templates = {}

def fetch_user_profile_picture(user_id):
    """Fetches the user's Telegram profile picture."""
    try:
        photos = bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            file_info = bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
            response = requests.get(file_url)
            profile_pic = Image.open(BytesIO(response.content)).convert("RGBA")
            return profile_pic
        else:
            return Image.new("RGBA", (200, 200), (128, 128, 128))  # Gray placeholder
    except Exception as e:
        print(f"Error fetching profile picture: {e}")
        return Image.new("RGBA", (200, 200), (128, 128, 128))  # Gray placeholder

def create_profile_picture_with_template(template_url, profile_picture):
    """Combines the user's profile picture with the selected template."""
    response = requests.get(template_url)
    template = Image.open(BytesIO(response.content)).convert("RGBA")

    # Resize and crop the profile picture to fit into a circular frame
    profile_picture = profile_picture.resize((80, 90))
    mask = Image.new("L", profile_picture.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((2.5, 2.5) + profile_picture.size, fill=255)
    profile_picture = ImageOps.fit(profile_picture, mask.size, centering=(3, 3))
    profile_picture.putalpha(mask)

    # Paste the profile picture onto the template
    template.paste(profile_picture, (40, 50), profile_picture)
    return template

@bot.message_handler(commands=["profile"])
def view_profile(message):
    """Sends the user's profile picture with the selected template."""
    user_id = message.from_user.id
    
    if not has_started_bot(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
        bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    if not is_user_updated(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('update',url='https://t.me/Auct_he_bot?start=update'))
        bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return
    
    try:
        user_id = message.from_user.id
        template_id = user_templates.get(user_id, 1)  # Default to template 1
        template_url = TEMPLATES.get(template_id, TEMPLATES[1])

        # Fetch and create profile picture
        profile_picture = fetch_user_profile_picture(user_id)
        combined_image = create_profile_picture_with_template(template_url, profile_picture)

        # Save image to BytesIO and send
        image_bytes = BytesIO()
        combined_image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username if message.from_user.username else "No Username"

        from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
        userd = str(user_id)
        bought_count = len(purchase_history.get(userd, []))
        sold_count = len(sales_history.get(userd, []))

        # Create inline button to change the profile picture
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Change Profile Picture", url="https://t.me/auct_he_bot?start=profile"))

        text = (
            "═════════════════════\n"
            f"🏅 𝖯𝖱𝖮𝖥𝖨𝖫𝖤 𝖨𝖭𝖥𝖮 🏅\n"
            "═════════════════════\n\n"
            f"👤 𝗡𝗮𝗺𝗲: {first_name}\n"
            f"🔗 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @{username if username else 'No Username'}\n"
            f"🆔 𝗨𝘀𝗲𝗿 𝗜𝗗: {user_id}\n\n"
            "═════════════════════\n"
            "🛒 𝗧𝗥𝗔𝗗𝗜𝗡𝗚 𝗔𝗖𝗧𝗜𝗩𝗜𝗧𝗬\n"
            "═════════════════════\n\n"
            f"📥 𝗜𝘁𝗲𝗺𝘀 𝗕𝗼𝘂𝗴𝗵𝘁: {bought_count}\n"
            f"📤 𝗜𝘁𝗲𝗺𝘀 𝗦𝗼𝗹𝗱: {sold_count}\n\n"
            "═════════════════════\n"
            "🔥 𝗞𝗲𝗲𝗽 𝗧𝗿𝗮𝗱𝗶𝗻𝗴 & 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 𝗨𝘀!\n"
            "═════════════════════"
        )
        bot.send_photo(
            chat_id=message.chat.id,
            photo=image_bytes,
            caption=text,
            reply_markup=markup,
            reply_to_message_id=message.message_id,
            has_spoiler=True
        )
    except Exception as e:
        print(f"Error in /profile: {e}")
        bot.reply_to(message, "An error occurred while processing your request.")

@bot.message_handler(commands=["setprofilepic"])
def set_profile_pic(message):
    user_id = message.from_user.id
    if not has_started_bot(user_id):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
        bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
        return

"""Allows users to set a new profile picture."""
    try:
        user_id = message.from_user.id
        send_template_options(user_id)
    except Exception as e:
        print(f"Error in /setprofilepic: {e}")
        bot.reply_to(message, "An error occurred while processing your request.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("template_"))
def handle_template_selection(call):
    """Handles template selection and updates the user's profile picture."""
    try:
        user_id = call.from_user.id
        _, original_user_id, template_id = call.data.split("_")
        original_user_id = int(original_user_id)
        template_id = int(template_id)

        if user_id != original_user_id:
            bot.answer_callback_query(call.id, "❌ This action is not intended for you.")
            return

        if template_id in TEMPLATES:
            user_templates[user_id] = template_id
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<blockquote><b>✅ 𝚃𝙴𝙼𝙿𝙻𝙰𝚃𝙴 {template_id} 𝚂𝙴𝙻𝙴𝙲𝚃𝙴𝙳 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈! </b></blockquote>",parse_mode='html')
            bot.answer_callback_query(call.id, "Template selected!")

            # Send updated profile picture
            profile_picture = fetch_user_profile_picture(user_id)
            combined_image = create_profile_picture_with_template(TEMPLATES[template_id], profile_picture)

            image_bytes = BytesIO()
            combined_image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            bot.send_photo(chat_id=call.message.chat.id, photo=image_bytes, caption="Here is your updated profile picture!",has_spoiler=True)
        else:
            bot.answer_callback_query(call.id, "❌ Invalid template selection.")
    except Exception as e:
        print(f"Error in handle_template_selection: {e}")
        bot.answer_callback_query(call.id, "An error occurred while processing your request.")

def send_template_options(user_id):
    """Sends template options to the user in a structured row format."""
    try:
        markup = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(f"{template_id}", callback_data=f"template_{user_id}_{template_id}") for template_id in TEMPLATES]

        # Add buttons in rows of 5
        for i in range(0, len(buttons), 5):
            markup.row(*buttons[i:i+5])  # Add 5 buttons per row

        bot.send_message(user_id, "Select a template for your profile picture:", reply_markup=markup)
    except Exception as e:
        print(f"Error in send_template_options: {e}")

nature_info = {
    "modest": {
        "increase": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘈𝘵𝘵𝘢𝘤𝘬",
        "decrease": "𝘈𝘵𝘵𝘢𝘤𝘬",
        "photo": "https://i.postimg.cc/HshBYmPH/IMG-20241228-161817-810.jpg"  # Example URL from PostImage
    },
    "bold": {
        "increase": "𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "decrease": "𝘈𝘵𝘵𝘢𝘤𝘬",
        "photo": "https://i.postimg.cc/ncqRFg7P/IMG-20241228-161758-388.jpg"
    },
    "timid": {
        "increase": "𝘚𝘱𝘦𝘦𝘥",
        "decrease": "𝘈𝘵𝘵𝘢𝘤𝘬",
        "photo": "https://i.postimg.cc/4xMfQYLM/IMG-20241228-161835-358.jpg"
    },
    "naive": {
        "increase": "𝘚𝘱𝘦𝘦𝘥",
        "decrease": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "photo": "https://i.postimg.cc/zDPcBTV9/IMG-20241228-161819-937.jpg"
    },
    "calm": {
        "increase": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "decrease": "𝘈𝘵𝘵𝘢𝘤𝘬",
        "photo": "https://i.postimg.cc/T38K9W5S/IMG-20241228-161802-132.jpg"
    },
    "hasty": {
        "increase": "𝘚𝘱𝘦𝘦𝘥",
        "decrease": "𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "photo": "https://i.postimg.cc/9M7X6hML/IMG-20241228-165756-787.jpg"
    },
    "brave": {
        "increase": "𝘈𝘵𝘵𝘢𝘤𝘬",
        "decrease": "𝘚𝘱𝘦𝘦𝘥",
        "photo": "https://i.postimg.cc/fTfGHGVN/IMG-20241228-161800-265.jpg"
    },
    "mild": {
        "increase": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘈𝘵𝘵𝘢𝘤𝘬",
        "decrease": "𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "photo": "https://i.postimg.cc/9fJvYKQf/IMG-20241228-161815-768.jpg"
    },
    "sassy": {
        "increase": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "decrease": "𝘚𝘱𝘦𝘦𝘥",
        "photo": "https://i.postimg.cc/XYQbsp23/IMG-20241228-161831-500.jpg"
    },
    "lax": {
        "increase": "𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "decrease": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "photo": "https://i.postimg.cc/wByGDvZw/IMG-20241228-161812-611.jpg"
    },
    "relaxed": {
        "increase": "𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "decrease": "𝘚𝘱𝘦𝘦𝘥",
        "photo": "https://i.postimg.cc/Y92LJG73/IMG-20241228-161828-397.jpg"
    },
    "bashful": {
        "increase": "𝘕𝘰𝘯𝘦",
        "decrease": "𝘕𝘰𝘯𝘦",
        "photo": "https://i.postimg.cc/xTLHNS6L/IMG-20241228-161757-079.jpg"
    },
    "quirky": {
        "increase": "𝘕𝘰𝘯𝘦",
        "decrease": "𝘕𝘰𝘯𝘦",
        "photo": "https://i.postimg.cc/R02VTWFh/IMG-20241228-161824-484.jpg"
    },
    "docile": {
        "increase": "𝘕𝘰𝘯𝘦",
        "decrease": "𝘕𝘰𝘯𝘦",
        "photo": "https://i.postimg.cc/Pf20GBWz/IMG-20241228-161805-126.jpg"
    },
    "gentle": {
        "increase": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "decrease": "𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "photo": "https://i.postimg.cc/zG1Cxfyd/IMG-20241228-161806-107.jpg"
    },
    "impish": {
        "increase": "𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "decrease": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘈𝘵𝘵𝘢𝘤𝘬",
        "photo": "https://i.postimg.cc/rpHDrj3t/IMG-20241228-161809-393.jpg"
    },
    "jolly": {
        "increase": "𝘚𝘱𝘦𝘦𝘥",
        "decrease": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘈𝘵𝘵𝘢𝘤𝘬",
        "photo": "https://i.postimg.cc/0yFvG45x/IMG-20241228-161810-601.jpg"
    },
    "lonely": {
        "increase": "𝘈𝘵𝘵𝘢𝘤𝘬",
        "decrease": "𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "photo": "https://i.postimg.cc/HLgZC0BX/IMG-20241228-161813-346.jpg"
    },
    "serious": {
        "increase": "𝘕𝘰𝘯𝘦",
        "decrease": "𝘕𝘰𝘯𝘦",
        "photo": "https://i.postimg.cc/KjSrnxwL/IMG-20241228-161833-838.jpg"
    },
    "rash": {
        "increase": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘈𝘵𝘵𝘢𝘤𝘬",
        "decrease": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "photo": "https://i.postimg.cc/HW97Sw7F/IMG-20241228-161826-488.jpg"
    },
    "quiet": {
        "increase": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘈𝘵𝘵𝘢𝘤𝘬",
        "decrease": "𝘚𝘱𝘦𝘦𝘥",
        "photo": "https://i.postimg.cc/ydvsR8kp/IMG-20241228-161823-342.jpg"
    },
    "hardy": {
        "increase": "𝘕𝘰𝘯𝘦",
        "decrease": "𝘕𝘰𝘯𝘦",
        "photo": "https://i.postimg.cc/DZJ3SP30/IMG-20241228-161807-859.jpg"
    },
    "careful": {
        "increase": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "decrease": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘈𝘵𝘵𝘢𝘤𝘬",
        "photo": "https://i.postimg.cc/dtpFKfbX/IMG-20241228-161803-023.jpg"
    },
    "naughty": {
        "increase": "𝘈𝘵𝘵𝘢𝘤𝘬",
        "decrease": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘋𝘦𝘧𝘦𝘯𝘴𝘦",
        "photo": "https://i.postimg.cc/2jtMqZ0L/IMG-20241228-161821-490.jpg"
    },
    "adamant": {
        "increase": "𝘈𝘵𝘵𝘢𝘤𝘬",
        "decrease": "𝘚𝘱𝘦𝘤𝘪𝘢𝘭 𝘈𝘵𝘵𝘢𝘤𝘬",
        "photo": "https://i.postimg.cc/MKpCFsVf/IMG-20241228-161755-038.jpg"
    }
}

@bot.message_handler(commands=['natures'])
def natures(message):
    if str(message.from_user.id) in banned:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        user_id = message.from_user.id
        if not has_started_bot(user_id):
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
            bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
            return
    
        if not is_user_updated(user_id):
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('update',url='https://t.me/Auct_he_bot?start=update'))
            bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
            return
        
        response = "Nature Types:\n"
        for nature in nature_info:
            response += f"- {nature.capitalize()}\n"
        bot.reply_to(message, response)

# Handler for nature-specific information
@bot.message_handler(func=lambda message: message.text.lower() in nature_info)
def handle_nature(message):
    nature_name = message.text.lower()
    info = nature_info[nature_name]
    response = f"""
    <blockquote>
┏━━━━《✮ {nature_name.capitalize()} ✮》
 ➥ {info['increase']} 🔺
 ➥ {info['decrease']} 🔻
 ▱▱▱▱▱▱▱▱▱▱
   Powered By <a href='https://t.me/Auct_he_bot'>𝘈𝘐𝘖 𝘈𝘜𝘊𝘛𝘐𝘖𝘕 𝘉𝘖𝘛 </a>
┗━━━━━━━━━━━━━━━━━━━
    </blockquote>
    """
    # Send nature stats and photo
    bot.send_photo(message.chat.id, info['photo'],caption=response,parse_mode="html")


tm_data = {
    2: {"name": "Dragon Claw", "power": 80, "accuracy": 100, "category": "P"},   
    3: {"name": "Psyshock", "power": 80, "accuracy": 100, "category": "S"},
    9: {"name": "Venoshock", "power": 65, "accuracy": 100, "category": "S"},
    10: {"name": "Hidden Power", "power": 60, "accuracy": 100, "category": "S"},
    13: {"name": "Ice Beam", "power": 90, "accuracy": 100, "category": "S"},
    14: {"name": "Blizzard", "power": 110, "accuracy": 70, "category": "S"},
    15: {"name": "Hyper Beam", "power": 150, "accuracy": 90, "category": "S"},
    22: {"name": "Solar Beam", "power": 120, "accuracy": 100, "category": "S"},
    23: {"name": "Smack Down", "power": 50, "accuracy": 100, "category": "P"},
    24: {"name": "Thunderbolt", "power": 90, "accuracy": 100, "category": "S"},
    25: {"name": "Thunder", "power": 110, "accuracy": 70, "category": "P"},
    26: {"name": "Earthquake", "power": 100, "accuracy": 100, "category": "P"},
    28: {"name": "Leech Life", "power": 80, "accuracy": 100, "category": "P"},
    29: {"name": "Psychic", "power": 90, "accuracy": 100, "category": "S"},
    30: {"name": "Shadow Ball", "power": 80, "accuracy": 100, "category": "S"},
    31: {"name": "Brick Break", "power": 75, "accuracy": 100, "category": "P"},
    34: {"name": "Sludge Wave", "power": 95, "accuracy": 100, "category": "S"},
    35: {"name": "Flamethrower", "power": 90, "accuracy": 100, "category": "S"},
    36: {"name": "Sludge Bomb", "power": 90, "accuracy": 100, "category": "S"},
    38: {"name": "Fire Blast", "power": 110, "accuracy": 85, "category": "S"},
    39: {"name": "Rock Tomb", "power": 60, "accuracy": 95, "category": "P"},
    40: {"name": "Aerial Ace", "power": 60, "accuracy": 100, "category": "P"},
    42: {"name": "Facade", "power": 70, "accuracy": 100, "category": "P"},
    43: {"name": "Flame Charge", "power": 50, "accuracy": 100, "category": "P"},
    46: {"name": "Thief", "power": 60, "accuracy": 100, "category": "P"},
    47: {"name": "Low Sweep", "power": 65, "accuracy": 100, "category": "P"},
    48: {"name": "Round", "power": 60, "accuracy": 100, "category": "S"},
    49: {"name": "Echoed Voice", "power": 40, "accuracy": 100, "category": "S"},
    50: {"name": "Overheat", "power": 130, "accuracy": 90, "category": "S"},
    51: {"name": "Steel Wing", "power": 70, "accuracy": 90, "category": "P"},
    52: {"name": "Focus Blast", "power": 120, "accuracy": 70, "category": "S"},
    53: {"name": "Energy Ball", "power": 90, "accuracy": 100, "category": "S"},
    54: {"name": "False Swipe", "power": 40, "accuracy": 100, "category": "P"},
    55: {"name": "Scald", "power": 80, "accuracy": 100, "category": "S"},
    57: {"name": "Charge Beam", "power": 50, "accuracy": 90, "category": "S"},
    58: {"name": "Sky Drop", "power": 60, "accuracy": 100, "category": "P"},
    59: {"name": "Brutal Swing", "power": 60, "accuracy": 100, "category": "P"},
    62: {"name": "Acrobatics", "power": 55, "accuracy": 100, "category": "P"},
    65: {"name": "Shadow Claw", "power": 70, "accuracy": 100, "category": "P"},
    66: {"name": "Payback", "power": 50, "accuracy": 100, "category": "P"},
    67: {"name": "Smart Strike", "power": 70, "accuracy": 100, "category": "P"},
    68: {"name": "Giga Impact", "power": 150, "accuracy": 90, "category": "P"},
    71: {"name": "Stone Edge", "power": 100, "accuracy": 80, "category": "P"},
    72: {"name": "Volt Switch", "power": 70, "accuracy": 100, "category": "S"},
    76: {"name": "Fly", "power": 90, "accuracy": 95, "category": "P"},
    78: {"name": "Bulldoze", "power": 60, "accuracy": 100, "category": "P"},
    79: {"name": "Frost Breath", "power": 60, "accuracy": 90, "category": "S"},
    80: {"name": "Rock Slide", "power": 75, "accuracy": 90, "category": "P"},
    81: {"name": "X-Scissor", "power": 80, "accuracy": 100, "category": "P"},
    82: {"name": "Dragon Tail", "power": 60, "accuracy": 90, "category": "P"},
    83: {"name": "Infestation", "power": 70, "accuracy": 100, "category": "S"},
    84: {"name": "Poison Jab", "power": 80, "accuracy": 100, "category": "P"},
    85: {"name": "Dream Eater", "power": 100, "accuracy": 100, "category": "S"},
    89: {"name": "U-Turn", "power": 70, "accuracy": 100, "category": "P"},
    91: {"name": "Flash Cannon", "power": 80, "accuracy": 100, "category": "S"},
    93: {"name": "Wild Charge", "power": 90, "accuracy": 100, "category": "P"},
    94: {"name": "Surf", "power": 90, "accuracy": 100, "category": "S"},
    95: {"name": "Snarl", "power": 55, "accuracy": 95, "category": "S"},
    97: {"name": "Dark Pulse", "power": 80, "accuracy": 100, "category": "S"},
    98: {"name": "Waterfall", "power": 80, "accuracy": 100, "category": "P"},
    99: {"name": "Dazzling Gleam", "power": 80, "accuracy": 100, "category": "S"},
}

@bot.message_handler(commands=['tm00'])
def handle_tm00(message):
    if str(message.from_user.id) in banned:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        user_id = message.from_user.id
        if not has_started_bot(user_id):
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('start',url='https://t.me/Auct_he_bot?start=start'))
            bot.reply_to(message, '<blockquote><b>start the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
            return
        
        if not is_user_updated(user_id):
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('update',url='https://t.me/Auct_he_bot?start=update'))
            bot.reply_to(message, '<blockquote><b>update the bot first.</b></blockquote>', parse_mode='html',reply_markup=markup,disable_web_page_preview=True)
            return
        
        tm_list = "\n".join(
            f"|{tm_number}| {tm_info['name']} |  {tm_info['power']}|{tm_info['accuracy']}|{tm_info['category']} |\n"
            for tm_number, tm_info in tm_data.items()
        )
        bot.reply_to(message, f"<blockquote>TM List:\n\n{tm_list}\n\n▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱</blockquote>",parse_mode="html")



@bot.message_handler(func=lambda message: re.match(r'tm\d{2}', message.text.lower()))
def handle_tm(message):
    match = re.match(r'tm(\d{2})', message.text.lower())
    tm_number = int(match.group(1))

    if tm_number not in tm_data:
        bot.reply_to(message, "TM not found. Please check the TM number and try again.")
        return

    tm_info = tm_data[tm_number]
    category = "Physical" if tm_info["category"] == "P" else "Special"
    response_message = f"""
<blockquote>╔══   《TM{tm_number} 💿》  ══╗
  ☛ {tm_info['name']} [{category}]
  Power: {tm_info['power']} Accuracy: {tm_info['accuracy']}
╚══   《TM{tm_number} 💿》  ══╝
  ▱▱▱▱▱▱▱▱▱▱
  Powered by <a href='https://t.me/Auct_he_bot'>𝘈𝘐𝘖 𝘈𝘜𝘊𝘛𝘐𝘖𝘕 𝘉𝘖𝘛</a>
┗━━━━━━━━━━━━━━━━━━━</blockquote>
   
    """

    # Send the static photo from UploadImage.com with TM details
    bot.send_photo(
        chat_id=message.chat.id,
        photo=TM_IMAGE_URL,
        caption=response_message,
        parse_mode="html")


@bot.message_handler(commands=['reset_items'])
def handle_reset_items(message):
    if str(message.from_user.id) not in admin_ids:
        bot.reply_to(message, "❌ You don't have permission to reset the auction items.")
        return

    global items, c, msg
    items = []  # Clear the items list
    c=0
    msg = []
    bot.reply_to(message, "✅ The auction items have been successfully reset.")


@bot.message_handler(commands=['remove_items'])
def handle_remove_items(message):
    if str(message.from_user.id) not in admin_ids:
        bot.reply_to(message, "❌ You don't have permission to remove items from the auction.")
        return

    try:
        pokemon_name = message.text.split(' ', 1)[1].strip()
    except IndexError:
        bot.reply_to(message, "⚠️ Please specify the Pokémon name to remove.\nExample: /remove Pikachu")
        return

    global items
    if pokemon_name in items:
        items.remove(pokemon_name)
        bot.reply_to(message, f"✅ '{pokemon_name}' has been removed from the auction items.")
    else:
        bot.reply_to(message, f"⚠️ '{pokemon_name}' is not in the auction items.")

@bot.message_handler(commands=['tsold'])
def handle_tsold(message):
    if message.from_user.id in banned_users:
        bot.reply_to(message, "❌ You are banned by an administrator.")
    else:
        if message.from_user.id in admin_id:
            try:
                command, *args = message.text.split(' ', 1)
                if len(args) != 1:
                    raise ValueError
                tms_name = args[0]
                if not message.reply_to_message:
                    raise ValueError

                username = message.reply_to_message.from_user.username
                amount = message.reply_to_message.text

                # Create the reply message in the desired format
                reply_message = f"""
🔊 𝗧𝗠𝗦 𝗦𝗢𝗟𝗗 🚀

<blockquote>𝗧𝗠𝗦 𝗡𝗔𝗠𝗘 -\n {tms_name}

🔸𝗦𝗢𝗟𝗗 𝗧𝗢 - @{username}
🔸𝗦𝗢𝗟𝗗 𝗙𝗢𝗥 - {amount}</blockquote>

❗<a href='https://t.me/AllinoneHexa'>Join Trade Group</a> To Get Seller Username After Auction
"""
                sent_message = bot.reply_to(message, reply_message, parse_mode="HTML", disable_web_page_preview=True)

                # Send a sticker to celebrate the sale
                bot.send_sticker(message.chat.id, SOLD_STICKER_ID)

                # Pin the sold message in the chat
                bot.pin_chat_message(message.chat.id, sent_message.id)

                # Track sold items
                tsold_items.append((tms_name, username, amount))

            except ValueError:
                # Handle invalid command usage
                bot.send_sticker(message.chat.id, DOUBT_STICKER_ID)
                bot.reply_to(
                    message,
                    "❌ <b>Invalid usage!</b> Please use the command in the format:\n<code>/tsold (TMS name)</code>",
                    parse_mode="HTML"
                )
        else:
            # Handle unauthorized users attempting to use the command
            bot.send_sticker(message.chat.id, ANGRY_STICKER_ID)
            bot.reply_to(
                message,
                "❌ <b>You are not authorized to use this command.</b>",
                parse_mode="HTML"
            )

tsold_items=[]


@bot.message_handler(commands=['tbuyers'])
def handle_tbuyers(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if message.from_user.id not in admin_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        if not tsold_items:
            bot.reply_to(message, "No items have been sold yet.")
            return

        buyers_list = "📋 List of Buyers:\n\n"
        for tms_name, buyer_username, amount in tsold_items:
            buyers_list += f"🔹 {tms_name} sold to @{buyer_username} for {amount}\n"

        bot.reply_to(message, buyers_list)


@bot.message_handler(commands=['reset_tbuyers'])
def reset_tbuyers(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if message.from_user.id not in admin_id:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        global tsold_items
        tsold_items.clear()  # Clear the buyers list
        bot.reply_to(message, "The buyers list has been reset.")


@bot.message_handler(commands=['remove_tbuyer'])
def remove_tbuyer(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "❌ You Are Banned By an Administrator.")
        return

    if message.from_user.id not in admin_id:
        bot.reply_to(message, "🚫 You are not authorized to use this command.")
        return

    # Extract the username from the command
    try:
        username_to_remove = message.text.split()[1]  # Expecting format: /remove_buyer @username
    except IndexError:
        bot.reply_to(message, "❗ Please provide a username to remove.\nUsage: `/remove_buyer @username`", parse_mode="Markdown")
        return

    global tsold_items
    # Find and remove the matching buyer
    for item in tsold_items:
        if item[1] == username_to_remove:  # Check if the username matches
            tsold_items.remove(item)
            bot.reply_to(message, f"✅ Buyer @{username_to_remove} has been removed from the list.")
            return

    bot.reply_to(message, f"⚠️ Buyer @{username_to_remove} not found in the list.")

@bot.message_handler(commands=['update'])
def update_prompt(message):
    userd = message.from_user.id
    if message.chat.type != 'private':
        bot.reply_to(
            message,
            "please click below button to go for update",
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('update',url='https://t.me/auct_he_bot?start=update'))
            )
        return
    
    pic = 'AgACAgQAAyEFAASBkeyOAAL09WfW7HIZPPLKorA4ltmGh9kzUNnnAAKDtzEbplu8Un0NeLOT25NjAQADAgADeAADNgQ'
    text = 'To update the bot click the button down.'
    chat_id = message.chat.id
    
    bot.send_photo(
        chat_id,
        photo=pic,
        caption=text,
        reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Update',callback_data=f'update_{chat_id}_{userd}'))
    )
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("update_"))
def call_bcv(call):
    dat = call.data.split('_')
    user_id = call.from_user.id
    first_name = call.from_user.full_name
    username = f'@{call.from_user.username}' if call.from_user.username else f'<a href="tg://user?id={user_id}">{first_name}</a>'
    chatd = int(dat[1])
    usered = int(dat[2])  # Extracted user ID as integer

    # Fetch user data correctly from `users` dictionary
    userd = users.get(str(usered), {})  # Get user data or an empty dict

    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Check if the user exists and is already updated
    if userd.get('version') == CURRENT_BOT_VERSION:
        bot.send_message(chatd, "✅ You already have the latest bot version.")
        return

    # Sending update message
    bro = bot.send_message(chatd, "🔄 Your bot is updating now...")
    time.sleep(2)

    # Countdown update message
    for i in range(5, 0, -1):
        bot.edit_message_text(
            chat_id=bro.chat.id,
            message_id=bro.message_id,
            text=f"⚙️ Updating bot in {i}..."
        )
        time.sleep(1)

    bot.delete_message(bro.chat.id, bro.message_id)

    # Update the user's version if they exist in the dictionary
    if str(usered) in users:
        users[str(usered)].update({
            "name": first_name,  # Update name
            "username": username,  # Update username
            "version": CURRENT_BOT_VERSION  # Update version
        })
        save_user(users)
    else:
        bot.send_message(chatd, "⚠️ Update failed. Please try again.")
        return  # Exit if user is not found

    time.sleep(3)
    bot.send_photo(
        chatd,
        photo='AgACAgQAAyEFAASBkeyOAAL0-mfW7VLcXsO59L5wup6iXOv6Bq5UAALOtjEbQ911UCHDAowlfJWrAQADAgADeQADNgQ',
        caption="✅ Your bot has been updated successfully!\nYou can now start using the new features. 🚀",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Trade Group', url='https://t.me/allinonehexa')
        )
    )

@bot.message_handler(commands=['getid'])
def get_file_id(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Please reply to a sticker or photo to get its ID.")
        return
    
    replied = message.reply_to_message
    
    if replied.sticker:  # If it's a sticker
        file_id = replied.sticker.file_id
        bot.reply_to(message, f"Sticker ID: `{file_id}`", parse_mode='Markdown')

    elif replied.photo:  # If it's a photo (photo has multiple sizes, take the last one)
        file_id = replied.photo[-1].file_id
        bot.reply_to(message, f"Photo ID: `{file_id}`", parse_mode='Markdown')

    else:
        bot.reply_to(message, "This command only works when replying to a sticker or a photo.")

import re

# ✅ Replace with your actual values
TRADE_GROUP_ID = -1002128413716  # Replace with the actual trade group ID

# ✅ Function to check if the message is a valid bid (numbers, numbers + 'k', or "/pass")
def is_valid_bid(text):
    return re.fullmatch(r"\d+(\.\d+)?[kK]?|/pass", text) is not None

# ✅ Function to check if the user is an admin (checks against the list)
def is_admin(user_id):
    return user_id in xmods

# ✅ Function to check if the user is a member of the trade group
def is_user_in_trade_group(user_id):
    try:
        member = bot.get_chat_member(TRADE_GROUP_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking user {user_id} in trade group: {e}")
        return False

# ✅ Check if the user has started the bot
def has_started_bot(user_id):
    users = load_user()
    return str(user_id) in users

def is_user_updated(user_id):
    """Check if the user's bot version matches the current bot version."""
    user_data = users.get(str(user_id), {})  # Fetch user data safely
    
    return user_data.get("version") == CURRENT_BOT_VERSION

@bot.message_handler(func=lambda message: True, content_types=["text"])
def filter_messages(message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    chat_id = message.chat.id

    global auce_active

    if not auce_active:
        return
    
    if chat_id != -1002022693265:
        return 

    # ✅ Skip admin messages
    if is_admin(user_id):
        return

    if is_valid_bid(message.text):
        # ✅ Check if the user has started the bot
        if not has_started_bot(user_id):
            bot.delete_message(chat_id, message.message_id)
            mention = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
            warning_text = (
                f"{mention}, please start the bot before participating in the auction! "
                f"➡️ <a href='https://t.me/auct_he_bot?start=start'>Start Bot</a>."
            )
            bot.send_message(chat_id, warning_text, disable_web_page_preview=True, parse_mode='html')
            return
        
        if not is_user_updated(user_id):
            bot.delete_message(chat_id, message.message_id)
            mention = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
            warning_text = (
                f"{mention}, please start the bot before participating in the auction! "
                f"➡️ <a href='https://t.me/auct_he_bot?start=update'>Update Bot</a>."
            )
            bot.send_message(chat_id, warning_text, disable_web_page_preview=True, parse_mode='html')
            return

        # ✅ Check if the user is in the trade group
        if not is_user_in_trade_group(user_id):
            bot.delete_message(chat_id, message.message_id)
            mention = f"<a href='tg://user?id={user_id}'>{full_name}</a>"
            warning_text = (
                f"{mention}, you haven't joined the <a href='https://t.me/AllinoneHexa'>Trade Group</a> yet!"
            )
            bot.send_message(chat_id, warning_text, disable_web_page_preview=True, parse_mode='html')
        return

    # ✅ Delete invalid bid messages
    bot.delete_message(chat_id, message.message_id)

@bot.message_handler(commands=['sellerinfo'])
def send_sellerinfo(message):
    if str(message.from_user.id) in banned_users:
        bot.reply_to(message, "You Are Banned By an Administrator")
    else:
        if message.chat.type == 'private':
            sellerinfo_message = """
🔺Formats For Use Seller Command:-

🔹To Find 0l Seller :-
/seller <pokename>
E.g. /seller slakoth, /seller Abra

🔹To Find 6l Seller:-
/seller 6l <pokename>
E.g. /seller 6l yveltal, /seller 6l mewtwo

🔹To Find Shiny Seller:-
/seller shiny <pokename>
E.g. /seller shiny ponyta, /seller shiny steelix

🔹To Find TMs Seller :-
/seller <tm>
E.g. /seller TM12, /seller TM73

🔹To Find Team Seller :-
/seller <teamname> Team
E.g. /seller HP Team, /seller Spa Team
"""
            bot.reply_to(message, sellerinfo_message)
        else:
            bot.reply_to(message, "This command can only be used in private messages.")
            
# Start bot polling
print("Bot is running...")

bot.skip_pending = True

user_ids = set()







