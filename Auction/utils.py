from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def is_user_admin(bot: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        status = member.status
        logger.info(f"Checking admin status for user {user_id} in chat {chat_id}: Status = {status}")
        is_admin = status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
        logger.info(f"User {user_id} is {'admin' if is_admin else 'not admin'}")
        return is_admin
    except Exception as e:
        logger.error(f"Error checking admin status for user {user_id} in chat {chat_id}: {type(e).__name__}: {str(e)}")
        return False