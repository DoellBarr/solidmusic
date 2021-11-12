import sys
import asyncio
from os import system, execle, environ

import heroku3

from configs import config
from dB.lang_utils import get_message as gm

from pyrogram import Client, filters, types
from git import Repo
from git.exc import InvalidGitRepositoryError


def generate_changelogs(repo, remote, active_branch):
    return "".join(
        f" [{c.committed_datetime.strftime('%d/%m/%y')}]: {c.summary} <{c.author}>\n"
        for c in repo.iter_commits(f"HEAD..{remote}/{active_branch}")
    )


@Client.on_message(filters.command("update") & filters.user(config.OWNER_ID))
async def update_repo(_, message: types.Message):
    chat_id = message.chat.id
    msg = await message.reply(gm(chat_id, "processing_update"))
    try:
        repo = Repo().init()
    except InvalidGitRepositoryError:
        repo = Repo()
    if config.HEROKU_APP_NAME or config.HEROKU_API_KEY:
        heroku = heroku3.from_key(config.HEROKU_API_KEY)
        heroku_app = None
        heroku_apps = heroku.apps()
        for app in heroku_apps:
            if app.name == config.HEROKU_APP_NAME:
                heroku_app = app
                break
        if not heroku_app:
            await msg.edit("heroku app not found")
            return repo.__del__()
        heroku_git_url = heroku_app.git_url.replace(
            "https://", f"https://api:{config.HEROKU_API_KEY}@"
        )
        origin = repo.create_remote("heroku", heroku_git_url)
        origin.fetch()
        origin.pull()
        print("good")
    else:
        origin = repo.create_remote(
            "upstream", "https://github.com/doellbarr/solidmusic"
        ) if "upstream" not in repo.remotes else repo.remote("upstream")
    origin.fetch()
    repo.create_head("master", origin.refs.master)
    repo.heads.main.set_tracking_branch(origin.refs.master)
    repo.heads.main.checkout(True)
    active_branch = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(active_branch)
    if config.HEROKU_APP_NAME or config.HEROKU_API_KEY:
        change_log = generate_changelogs(repo, "heroku", active_branch)
    else:
        change_log = generate_changelogs(repo, "upstream", active_branch)
    if change_log:
        system("git pull -f pip3 install --no-cache-dir -r requirements.txt")
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        return
    await msg.edit(gm(chat_id, "already_newest"))
    await asyncio.sleep(5)
    await msg.delete()
    return repo.__del__()
