import re
from typing import Union

from pyrogram.types import InlineKeyboardMarkup, Message

from dB.lang_utils import get_message as gm
from . import bot as pyro_bot


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
        try:
            rex = re.findall(r"[Bb][Oo][Tt]", me.first_name)[0]
        except IndexError:
            rex = ""
        if rex:
            bot_name = me.first_name
        else:
            bot_name = f"{me.first_name} bot"
        bot_id = me.id
        return bot_username, bot_name, bot_id

    async def send_message(
        self,
        message: Message,
        key: str,
        format_key: str = "",
        reply_message: bool = False,
        markup: InlineKeyboardMarkup = None,
    ):
        """
        :param message: Message object
        :param key: get it from key in .json file in lang folder
        :param format_key: use it if the value in .json key has `{}` text
        :param reply_message: fill it with `boolean`
        :param markup: fill it with `InlineKeyboardMarkup`
        :return:
        """
        chat_id = message.chat.id
        if not reply_message:
            return await self._bot.send_message(
                chat_id,
                gm(chat_id, key).format(format_key),
                disable_web_page_preview=True,
                reply_markup=markup,
            )
        return await message.reply(
            gm(chat_id, key).format(format_key),
            disable_web_page_preview=True,
            reply_markup=markup,
        )

    async def get_user_mention(self, chat_id: int, user_id: Union[str, int]):
        bot = self._bot
        member = await bot.get_chat_member(chat_id, user_id)
        return member.user.mention

    async def send_to_chat(
        self,
        chat_id: int,
        key: str,
        format_key: str = "",
        markup: InlineKeyboardMarkup = None,
    ):
        return await self._bot.send_message(
            chat_id,
            gm(chat_id, key).format(format_key),
            disable_web_page_preview=True,
            reply_markup=markup,
        )

    async def start(self):
        return await self._bot.start()

    async def stop(self):
        return await self._bot.stop()


bot_client = Bot()
