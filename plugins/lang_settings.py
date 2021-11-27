from pyrogram import Client, filters, types

from core.bot import Bot
from database.chat_database import ChatDB
from database.lang_utils import kode, lang_flags

from functions.decorators import authorized_only


@Client.on_message(filters.command("lang"))
@authorized_only
async def change_lang_(_, message: types.Message):
    chat_id = message.chat.id
    try:
        lang = message.command[1]
    except IndexError:
        lang = ""
    if not lang:
        temp = []
        keyboard = []
        for count, lang in enumerate(kode, start=1):
            flag = lang_flags[lang]
            temp.append(
                types.InlineKeyboardButton(flag, callback_data=f"set_lang_{lang}")
            )
            if count % 2 == 0:
                keyboard.append(temp)
                temp = []
            if count == len(kode):
                keyboard.append(temp)
        return await Bot().send_message(
            chat_id, "supported_lang", markup=types.InlineKeyboardMarkup(keyboard)
        )
    if len(lang) == 1:
        return await Bot().send_message(chat_id, "invalid_lang")
    if len(lang) >= 2 and lang in kode:
        x = ChatDB().set_lang(chat_id, lang)
        return await Bot().send_message(chat_id, x, lang)


__cmds__ = ["lang"]
__help__ = {
    "lang": "help_lang"
}
