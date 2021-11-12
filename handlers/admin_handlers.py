import asyncio
import sys

import heroku3
from pyrogram import Client, filters, types

from git import Repo
from git.exc import InvalidGitRepositoryError
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


def get_heroku_git_url(api_key: str, app_name: str):
    if not api_key or app_name:
        return None
    heroku = heroku3.from_key(api_key)
    heroku_apps = heroku.apps()
    app = None
    for heroku_app_name in heroku_apps:
        if heroku_app_name.name == app_name:
            app = heroku_app_name
            break
    return app.git_url.replace("https://", f"https://api:{api_key}@")


@Client.on_message(filters.command("update") & filters.user(config.OWNER_ID))
async def update_repo(_, message: types.Message):
    chat_id = message.chat.id
    heroku_git_url = get_heroku_git_url(config.HEROKU_API_KEY, config.HEROKU_APP_NAME)
    msg = await message.reply(gm(chat_id, "processing_update"))
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "upstream" in repo.remotes:
            origin = repo.remote("upstream")
        else:
            origin = repo.create_remote("upstream", heroku_git_url)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.main.set_tracking_branch(origin.refs.master)
        repo.heads.main.checkout(True)
    active_branch = repo.active_branch.name
    repo.remote("upstream").fetch(active_branch)
    change_log = "".join(
        f" [{c.committed_datetime.strftime('%d/%m/%y')}]: {c.summary} <{c.author}>\n"
        for c in repo.iter_commits(f"HEAD..upstream/{active_branch}")
    )
    if change_log:
        system("git pull -f pip3 install --no-cache-dir -r requirements.txt")
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
