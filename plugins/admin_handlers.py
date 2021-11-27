import sys

from pyrogram import Client, filters, types

from configs import config
from core.bot import Bot
from core.player import player
from functions.decorators import authorized_only
from os import execle, environ
from database.lang_utils import get_message as gm


@Client.on_message(filters.command("pause"))
@authorized_only
async def pause(_, message: types.Message):
    chat_id = message.chat.id
    stats = await player.change_streaming_status("pause", chat_id)
    return await Bot().send_message(
        chat_id,
        stats,
    )


@Client.on_message(filters.command("resume"))
@authorized_only
async def resume_(_, message: types.Message):
    chat_id = message.chat.id
    stats = await player.change_streaming_status("resume", chat_id)
    return await Bot().send_message(chat_id, stats)


@Client.on_message(filters.command("skip"))
@authorized_only
async def skip_(_, message: types.Message):
    chat_id = message.chat.id
    await player.change_stream(chat_id)


@Client.on_message(filters.command(["vol", "volume"]))
@authorized_only
async def change_vol_(_, message: types.Message):
    chat_id = message.chat.id
    vol = int(message.command[1])
    await player.change_vol(chat_id, vol)


@Client.on_message(filters.command("end"))
@authorized_only
async def end_stream_(_, message: types.Message):
    chat_id = message.chat.id
    key = await player.end_stream(chat_id)
    first_name = (await message.chat.get_member(message.from_user.id)).user.first_name
    return await Bot().send_message(chat_id, key, first_name)


@Client.on_message(filters.command("restart") & filters.user(config.OWNER_ID))
async def restart_bot_(client: Client, message: types.Message):
    chat_id = message.chat.id
    msg = await message.reply(gm(chat_id, "restart_bot"))
    args = [sys.executable, "main.py"]
    await msg.edit(gm(chat_id, "restarted"))
    execle(sys.executable, *args, environ)
    await client.send_message(chat_id, "Hi, I'm Alive")
    return


__cmds__ = [
    "pause",
    "resume",
    "skip",
    "volume",
    "end",
    "restart"
]
__help__ = {
    "pause": "help_pause",
    "resume": "help_resume",
    "skip": "help_skip",
    "volume": "help_volume",
    "end": "help_end",
    "restart": "help_restart"
}
