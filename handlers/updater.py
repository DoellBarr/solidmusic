import sys
import asyncio
from os import system, execle, environ

import heroku3

from configs import config
from dB.lang_utils import get_message as gm

from pyrogram import Client, filters, types
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError, GitCommandError


def gen_chlog(repo, diff):
    upstream_repo_url = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = tldr_log = ""
    ch = f"<b>updates for <a href={upstream_repo_url}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b><a href={upstream_repo_url.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    off_repo = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    try:
        repo = Repo()
    except NoSuchPathError as error:
        print(f"directory {error} is not found")
        Repo().__del__()
        return
    except GitCommandError as error:
        print(f"Early failure! {error}")
        Repo().__del__()
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.main.set_tracking_branch(origin.refs.master)
        repo.heads.main.checkout(True)
    ac_br = repo.active_branch.name
    try:
        repo.create_remote("upstream", off_repo)
    except Exception as er:
        print(er)
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


@Client.on_message(filters.command("update") & filters.user(config.OWNER_ID))
async def update_repo(_, message: types.Message):
    chat_id = message.chat.id
    msg = await message.reply(gm(chat_id, "processing_update"))
    update_avail = updater()
    branch = (Repo.init()).active_branch
    if update_avail:
        system("git pull -f && pip3 install -r requirements.txt")
        await msg.edit(gm(chat_id, "success_update"))
        execle(sys.executable, sys.executable, "main.py", environ)
        return
    await msg.edit(gm(chat_id, "already_newest"))
