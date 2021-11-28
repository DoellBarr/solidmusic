from . import paginate_module, load_module, modules
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.lang_utils import get_message as gm, get_message


@Client.on_message(filters.command("help"))
async def help_cmds_(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    load_module(user_id)
    keyboard = paginate_module(chat_id, user_id)
    await message.reply(
        get_message(chat_id, "here_all_commands"),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    modules.clear()
    keyboard.clear()


__cmds__ = ["help"]
__help__ = {
    "help": "help_help"
}
