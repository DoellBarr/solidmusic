from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from solidmusic.core.client import Client
from pyrogram.types import Message
from solidmusic.database.chat_db import chat_db
from solidmusic.database.lang_utils import list_lang, lang_flags, gm
from solidmusic.functions.decorators import authorized_only


@Client.on_message(filters.command("lang"))
@authorized_only
async def change_lang_(_, message: Message):
    chat_id = message.chat.id
    print(message)
    try:
        lang = message.command[1]
    except IndexError:
        lang = ""
    if not lang:
        temp = []
        keyboard = []
        for count, lang in enumerate(list_lang, start=1):
            flag = lang_flags[lang]
            temp.append(InlineKeyboardButton(flag, callback_data=f"set_lang_{lang}"))
            if count % 2 == 0:
                keyboard.append(temp)
                temp = []
            if count == len(list_lang):
                keyboard.append(temp)
        return await message.reply(
            await gm(chat_id, "supported_lang"),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    if len(lang) == 1:
        return await message.reply(await gm(chat_id, "invalid_lang"))
    if len(lang) >= 2 and lang in list_lang:
        x = await chat_db.set_lang(chat_id, lang)
        return await message.reply(await gm(chat_id, x, [lang]))


__cmds__ = ["lang"]
__help__ = {"lang": "help_lang"}
