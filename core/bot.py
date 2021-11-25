import asyncio
from typing import Optional

from pyrogram.errors import ChatAdminRequired
from pyrogram.types import InlineKeyboardMarkup

from .clients import bot
from database.lang_utils import get_message as gm


class Bot:
    def __init__(self):
        self._bot = bot

    async def promote_member(self, chat_id: int, user_id: int):
        try:
            await self._bot.promote_chat_member(
                chat_id, user_id, can_manage_voice_chats=True
            )
        except ChatAdminRequired:
            return await self.send_message(chat_id, "not_an_admin")

    async def send_message(
        self,
        chat_id: int,
        key: str,
        format_key: str = "",
        markup: InlineKeyboardMarkup = None,
        delete: Optional[int] = 0
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
        return (await self._bot.export_chat_invite_link(chat_id)).invite_link

    async def get_me(self):
        return await self._bot.get_me()

    async def get_user_mention(self, user_id: int):
        return (await self._bot.get_users(user_id)).mention

    async def start(self):
        return await self._bot.start()

    async def stop(self):
        return await self._bot.stop()
