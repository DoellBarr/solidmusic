import re
from typing import Union
from . import bot as pyro_bot

from dB.lang_utils import get_message as gm

from pyrogram.types import InlineKeyboardMarkup


class Bot:
    def __init__(self):
        self._bot = pyro_bot

    async def get_my(self):
        """
        Make bot get the necessary things only

        :return: bot_username, bot_name, bot_id
        """
        bot = self._bot
        me = await bot.get_me()
        bot_username = me.username
        rex = re.findall(r"[Bb][Oo][Tt]", me.first_name)[0]
        bot_name = f"{me.first_name if me.first_name.endswith(rex) else me.first_name + ' bot'}"
        bot_id = me.id
        return bot_username, bot_name, bot_id

    async def send_message(
            self,
            chat_id: int,
            key: str,
            reply_message: int = 0,
            format_key: str = "",
            disable_preview: bool = False,
            markup: InlineKeyboardMarkup = None
    ):
        """
        :param chat_id: fill with chat_id
        :param key: fill with key from .json file in lang directory
        :param reply_message: fill this with message_id if you want to bot replying to message
        :param format_key: fill with a value if necessary
        :param disable_preview: fill it as boolean if you want to your bot is disable or enabling web page preview
        :param markup: fill it with InlineKeyboardMarkup only
        :return:
        """
        bot = self._bot
        if not reply_message:
            return await bot.send_message(
                chat_id,
                gm(chat_id, key).format(format_key),
                disable_web_page_preview=disable_preview,
                reply_markup=markup
            )
        return await bot.send_message(
            chat_id,
            gm(chat_id, key).format(format_key),
            disable_web_page_preview=disable_preview,
            reply_markup=markup,
            reply_to_message_id=reply_message
        )

    async def get_user_mention(
            self,
            chat_id: int,
            user_id: Union[str, int]
    ):
        bot = self._bot
        member = await bot.get_chat_member(chat_id, user_id)
        return member.user.mention


bot_client = Bot()
