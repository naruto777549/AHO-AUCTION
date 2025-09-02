from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def is_user_admin(bot: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        status = member.status
        logger.info(f"Checking admin status for user {user_id} in chat {chat_id}: Status = {status}")

        # ✅ Handle all possible admin/owner statuses
        if status in [
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,      # v2.x
            ChatMemberStatus.CREATOR     # older versions
        ]:
            return True

        # Extra fallback string check
        if str(status).lower() in ["administrator", "owner", "creator"]:
            return True

        return False

    except Exception as e:
        logger.error(f"Error checking admin status for user {user_id} in chat {chat_id}: {type(e).__name__}: {e}")
        return False