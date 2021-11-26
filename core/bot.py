import asyncio
from typing import Optional, Union

from pyrogram.types import InlineKeyboardMarkup, ChatInviteLink

from .clients import bot
from database.lang_utils import get_message as gm


class Bot:
    def __init__(self):
        self._bot = bot

    async def promote_member(self, chat_id: int, user_id: int):
        return await self._bot.promote_chat_member(
            chat_id, user_id, can_manage_voice_chats=True
        )

    async def unban_member(self, chat_id: int, user_id: int):
        return await self._bot.unban_chat_member(
            chat_id, user_id
        )

    async def send_message(
        self,
        chat_id: int,
        key: str,
        format_key: str = "",
        markup: InlineKeyboardMarkup = None,
        delete: Optional[int] = 10,
    ):
        msg = await self._bot.send_message(
            chat_id,
            gm(chat_id, key).format(format_key),
            reply_markup=markup,
            disable_web_page_preview=True,
        )
        if delete:
            await asyncio.sleep(delete)
            return await msg.delete()
        return msg

    async def export_chat_invite_link(self, chat_id: int):
        link = await self._bot.create_chat_invite_link(chat_id, member_limit=1)
        try:
            return link.invite_link
        except AttributeError:
            return link

    async def revoke_chat_invite_link(self, chat_id: int, invite_link: Union[str, ChatInviteLink]):
        return await self._bot.revoke_chat_invite_link(chat_id, invite_link)

    async def get_me(self):
        return await self._bot.get_me()

    async def get_user_mention(self, user_id: int):
        return (await self._bot.get_users(user_id)).mention

    async def start(self):
        return await self._bot.start()

    async def stop(self):
        return await self._bot.stop()
