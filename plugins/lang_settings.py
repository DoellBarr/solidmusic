from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from base.bot_base import bot_client as bot

from dB.database import db
from dB.lang_utils import kode, lang_flags
from utils.functions.decorators import authorized_only


@Client.on_message(filters.command("lang"))
@authorized_only
async def change_lang_(_, message: Message):
    try:
        lang = message.command[1]
    except IndexError:
        lang = ""
    if len(lang) == 1:
        return await bot.send_message(message, "error_lang_cmd", reply_message=True)
    if not lang:
        temp = []
        keyboard = []
        for count, lang in enumerate(kode, start=1):
            flag = lang_flags[lang]
            temp.append(InlineKeyboardButton(flag, callback_data=f"set_lang_{lang}"))
            if count % 2 == 0:
                keyboard.append(temp)
                temp = []
            if count == len(kode):
                keyboard.append(temp)
        return await bot.send_message(
            message,
            "supported_lang",
            reply_message=True,
            markup=InlineKeyboardMarkup(keyboard),
        )
    if len(lang) >= 2:
        if lang in kode:
            x = db.set_chat_lang(message.chat.id, lang)
            if x:
                return await bot.send_message(
                    message, "lang_changed", reply_message=True
                )
        else:
            return await bot.send_message(
                message, "not_supported_lang", reply_message=True
            )
