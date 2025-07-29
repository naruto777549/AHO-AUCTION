import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

admin_id = list(map(int, os.getenv("ADMIN_ID", "").split(",")))
xmods = list(map(int, os.getenv("XMODS", "").split(",")))

WELCOME_STICKER_ID = os.getenv("WELCOME_STICKER_ID")
WARNING_STICKER_ID = os.getenv("WARNING_STICKER_ID")
SOLD_STICKER_ID = os.getenv("SOLD_STICKER_ID")
THINK_STICKER_ID = os.getenv("THINK_STICKER_ID")
ANGRY_STICKER_ID = os.getenv("ANGRY_STICKER_ID")
DOUBT_STICKER_ID = os.getenv("DOUBT_STICKER_ID")
SAD_STICKER_ID = os.getenv("SAD_STICKER_ID")
OK_STICKER_ID = os.getenv("OK_STICKER_ID")

AUCTION_GROUP_LINK = os.getenv("AUCTION_GROUP_LINK")
log_channel = int(os.getenv("LOG_CHANNEL"))
post_channel = int(os.getenv("POST_CHANNEL"))
approve_channel = int(os.getenv("APPROVE_CHANNEL"))
reject_channel = int(os.getenv("REJECT_CHANNEL"))

CURRENT_BOT_VERSION = os.getenv("CURRENT_BOT_VERSION", "3.0.0")
USER_DATA_FILE = os.getenv("USER_DATA_FILE", "users.json")