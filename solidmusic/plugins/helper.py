from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from solidmusic.core.client import Client
from solidmusic.core.types import Message
from solidmusic.database.lang_utils import gm
from solidmusic.plugins import modules, paginate_module, load_module


@Client.on_message(filters.command("help"))
async def help_cmds_(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if modules:
        modules.clear()
    load_module(user_id)
    keyboard = paginate_module(chat_id, user_id)
    keyboard.pop(-1)
    keyboard[-1].append(
        InlineKeyboardButton(
            f"🗑️ {await gm(chat_id, 'close_btn_name')}", f"close|{user_id}"
        )
    )
    await message.reply(
        "here_all_commands", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    modules.clear()
    keyboard.clear()


__cmds__ = ["help"]
__help__ = {"help": "help_help"}
