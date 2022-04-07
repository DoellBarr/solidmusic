import asyncio
import sys
from os import execle, environ

from configs import config

from solidmusic.core import types
from solidmusic.core.client import Client
from solidmusic.core.player import player
from solidmusic.functions.decorators import authorized_only
from solidmusic.database.lang_utils import gm

from pyrogram import filters


@Client.on_message(filters.command(["pause", "resume"]))
@authorized_only
async def pause_or_resume(_, m: types.Message):
    return await player.change_streaming_status(m.command[1], m)


@Client.on_message(filters.command("skip"))
@authorized_only
async def skip(_, m: types.Message):
    return await player.change_stream(m)


@Client.on_message(filters.command(["vol", "volume"]))
@authorized_only
async def change_vol(_, m: types.Message):
    return await player.change_vol(m)


@Client.on_message(filters.command("end"))
@authorized_only
async def end_stream(_, m: types.Message):
    return await player.end_stream(m)


@Client.on_message(filters.command("restart") & filters.user(config.owner_id))
async def restart_bot(_, m: types.Message):
    chat_id = m.chat.id
    msg = await m.reply("restart_bot")
    await asyncio.sleep(3)
    await msg.edit(await gm(chat_id, "restarted"))
    args = [sys.executable, "main.py"]
    execle(sys.executable, *args, environ)


__cmds__ = ["pause", "resume", "skip", "volume", "end", "restart"]
__help__ = {
    "pause": "help_pause",
    "resume": "help_resume",
    "skip": "help_skip",
    "volume": "help_volume",
    "end": "help_end",
    "restart": "help_restart",
}
