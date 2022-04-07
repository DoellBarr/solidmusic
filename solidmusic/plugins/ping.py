from time import time

from pyrogram import filters

from solidmusic.core.client import Client, call_py
from solidmusic.core.types import Message
from solidmusic.database.lang_utils import gm


@Client.on_message(filters.command("ping"))
async def check_ping_(_, message: Message):
    chat_id = message.chat.id
    start = time()
    msg = await message.reply("ping_text")
    pytgcalls_latency = await call_py.ping
    pyrogram_latency = time() - start
    await msg.edit(
        await gm(
            chat_id,
            "pong_text",
            [round(pyrogram_latency * 1000, 3), round(pytgcalls_latency, 2)],
        )
    )


__cmds__ = ["ping"]
__help__ = {"ping": "help_ping"}
