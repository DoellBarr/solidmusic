import asyncio
import sys

from pyrogram import Client, filters, types

from git import Repo, InvalidGitRepositoryError
from base.bot_base import bot_client as bot
from base.player import player
from configs import config
from utils.functions.decorators import authorized_only
from dB.lang_utils import get_message as gm
from os import execle, system, environ


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
        await bot.send_message(message, "track_ended", reply_message=True)
    return await bot.send_message(message, "not_streaming", reply_message=True)


@Client.on_message(filters.command("update") & filters.user(config.OWNER_ID))
async def update_repo(_, message: types.Message):
    chat_id = message.chat.id
    msg = await message.reply(gm(chat_id, "processing_update"))
    try:
        repo = Repo().init()
    except InvalidGitRepositoryError as error:
        print(error)
        repo = Repo().init()
    if "upstream" in repo.remotes:
        origin = repo.remote("upstream")
    else:
        origin = repo.create_remote("upstream", "https://github.com/DoellBarr/solidmusic")
    repo.create_head("master", origin.refs.master)
    repo.heads["master"].set_tracking_branch(origin.refs.master)
    repo.heads["master"].checkout(True)
    active_branch = repo.active_branch.name
    origin.fetch(active_branch)
    change_log = "".join(
        f" [{c.committed_datetime.strftime('%d/%m/%y')}]: {c.summary} <{c.author}>\n"
        for c in repo.iter_commits(f"HEAD..upstream/{active_branch}")
    )
    if change_log:
        await msg.edit(gm(chat_id, "start_update"))
        origin.pull(active_branch)
        await msg.edit(gm(chat_id, "success_update"))
        system("pip3 install --no-cache-dir -r requirements.txt")
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        return
    await msg.edit(gm(chat_id, "already_newest"))
    await asyncio.sleep(5)
    await msg.delete()
    return repo.__del__()


@Client.on_message(filters.command("restart"))
async def restart_bot_(_, message: types.Message):
    msg = await message.reply("restarting")
    args = [sys.executable, "main.py"]
    await msg.edit("restarted, now you can use this bot again.")
    execle(sys.executable, *args, environ)
    return
