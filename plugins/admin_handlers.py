import sys

from pyrogram import Client, filters, types
from base.bot_base import bot_client as bot
from base.player import player
from utils.functions.decorators import authorized_only
from os import execle, environ


@Client.on_message(filters.command("pause"))
@authorized_only
async def pause(_, message: types.Message):
    chat_id = message.chat.id
    stats = await player.change_streaming_status("pause", chat_id)
    return await bot.send_message(message, stats, reply_message=True)


@Client.on_message(filters.command("resume"))
@authorized_only
async def resume_(_, message: types.Message):
    chat_id = message.chat.id
    stats = await player.change_streaming_status("resume", chat_id)
    return await bot.send_message(message, stats, reply_message=True)


@Client.on_message(filters.command("skip"))
@authorized_only
async def skip_(_, message: types.Message):
    chat_id = message.chat.id
    toxt, title = await player.change_stream(chat_id)
    return await bot.send_message(message, toxt, title, reply_message=True)


@Client.on_message(filters.command(["vol", "volume"]))
@authorized_only
async def change_vol_(_, message: types.Message):
    chat_id = message.chat.id
    vol = int(message.command[1])
    check = await player.change_vol(chat_id, vol)
    if check:
        return await bot.send_message(message, "vol_changed", str(vol), True)
    return await bot.send_message(message, "not_streaming", reply_message=True)


@Client.on_message(filters.command("end"))
@authorized_only
async def end_stream_(_, message: types.Message):
    chat_id = message.chat.id
    check_call = await player.end_stream(chat_id)
    first_name = (await message.chat.get_member(message.from_user.id)).user.first_name
    if check_call:
        return await bot.send_message(message, "track_ended", first_name, reply_message=True)
    return await bot.send_message(message, "not_streaming", reply_message=True)


@Client.on_message(filters.command("restart"))
@authorized_only
async def restart_bot_(_, message: types.Message):
    msg = await message.reply("restarting")
    args = [sys.executable, "main.py"]
    await msg.edit("restarted, now you can use this bot again.")
    execle(sys.executable, *args, environ)
    return

