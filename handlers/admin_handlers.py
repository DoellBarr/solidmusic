import sys

from pyrogram import Client, filters, types
from base.bot_base import bot_client as bot
from base.player import player
from configs import config
from utils.functions.decorators import authorized_only
from git import Repo
from os import execle, system


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


@Client.on_message(filters.command("vol"))
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
    if check_call:
        return await bot.send_message(message, "track_ended", reply_message=True)
    return await bot.send_message(message, "not_streaming", reply_message=True)


@Client.on_message(filters.command("update") & filters.user(config.OWNER_ID))
async def update_repo(_, message: types.Message):
    msg = await message.reply("**processing...**")
    repo = Repo().init()
    if "origin" in repo.remotes:
        origin = repo.remote("origin")
    else:
        origin = repo.create_remote("origin", "https://github.com/DoellBarr/solidmusic")
    origin.fetch()
    origin.pull()
    system("pip3 install --no-cache-dir -r requirements.txt")
    await msg.edit("**update finished, now deploying**")
    args = [sys.executable, "main.py"]
    execle(sys.executable, *args)
    sys.exit()
