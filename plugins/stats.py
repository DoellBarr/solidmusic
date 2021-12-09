import platform
import shutil
import psutil

from pyrogram import Client, filters
from pyrogram.types import Message

from core import __version__ as bot_version
from sys import version
from pyrogram import __version__ as pyrogram_version
from pytgcalls.__version__ import __version__ as pytgcalls_version
from database.chat_database import ChatDB
from database.lang_utils import get_message as gm
from functions.stats_utils import humanbytes


@Client.on_message(filters.command("stats"))
async def get_stats_(client: Client, m: Message):
    bot_name = (await client.get_me()).first_name
    python_version = version.split(" ")[0]
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = f"{psutil.cpu_percent()} %"
    ram_usage = f"{psutil.virtual_memory().percent} %"
    pm, chats = ChatDB().get_stats()
    system_platform = platform.system()
    architecture_machine = platform.machine()
    chat_id = m.chat.id
    text = gm(chat_id, "stats_text").format(
        bot_name,
        bot_version,
        pytgcalls_version,
        pyrogram_version,
        python_version,
        chats,
        pm,
        cpu_usage,
        ram_usage,
        used,
        free,
        total,
        architecture_machine,
        system_platform
    )
    await m.reply(text, disable_web_page_preview=True)


__cmds__ = ["stats"]
__help__ = {
    "stats": "help_stats"
}
