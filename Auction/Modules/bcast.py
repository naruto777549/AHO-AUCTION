import asyncio
from telegram import Update, Message as TGMessage
from telegram.ext import Application, CommandHandler, ContextTypes
from config import ADMINS
from Auction.db import get_all_users, get_all_groups

async def broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Admin check
    if user_id not in ADMINS:
        return await update.message.reply_text("❌ You are not authorized to use this command.")

    # Determine broadcast content
    if update.message.reply_to_message:
        content: TGMessage = update.message.reply_to_message
    else:
        text = update.message.text.split(None, 1)
        if len(text) < 2:
            return await update.message.reply_text(
                "❌ ᴇxᴀᴍᴘʟᴇ:\n\n`/bcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]`",
                parse_mode="Markdown"
            )
        content = text[1]

    status = await update.message.reply_text("» sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...")
    total, pinned = 0, 0

    # ✅ Broadcast to Users
    users = await get_all_users()
    for user in users:
        try:
            if isinstance(content, TGMessage):
                await content.copy(user["_id"])
            else:
                await context.bot.send_message(user["_id"], content)
            total += 1
            await asyncio.sleep(0.03)
        except:
            continue

    # ✅ Broadcast to Groups
    groups = await get_all_groups()
    for group in groups:
        group_id = group["_id"]
        try:
            if isinstance(content, TGMessage):
                sent = await content.copy(group_id)
            else:
                sent = await context.bot.send_message(group_id, content)
            total += 1

            # Pin message in groups
            try:
                await sent.pin(disable_notification=True)
                pinned += 1
            except:
                pass

            await asyncio.sleep(0.03)
        except:
            continue

    await status.edit_text(
        f"✅ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ `{total}` ᴄʜᴀᴛs\n"
        f"📌 ᴍᴇssᴀɢᴇ ᴘɪɴɴᴇᴅ ɪɴ `{pinned}` ɢʀᴏᴜᴘs.",
        parse_mode="Markdown"
    )

def register(application: Application):
    application.add_handler(CommandHandler("bcast", broadcast_handler))