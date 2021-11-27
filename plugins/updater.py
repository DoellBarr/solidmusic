import sys
from os import system, execle, environ

from git import Repo
from git.exc import InvalidGitRepositoryError
from pyrogram import Client, filters, types

from configs import config
from database.lang_utils import get_message as gm


def gen_chlog(repo, diff):
    upstream_repo_url = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = tldr_log = ""
    ch = f"<b>updates for <a href={upstream_repo_url}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b>"
            f"<a href={upstream_repo_url.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        )
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", config.UPSTREAM_REPO)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if "upstream" in repo.remotes:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", config.UPSTREAM_REPO)
    ups_rem.fetch(ac_br)
    changelog, _ = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


@Client.on_message(filters.command("update") & filters.user(config.OWNER_ID))
async def update_repo(_, message: types.Message):
    chat_id = message.chat.id
    msg = await message.reply(gm(chat_id, "processing_update"))
    update_avail = updater()
    if update_avail:
        await msg.edit(gm(chat_id, "success_update"))
        system("git pull -f && pip3 install -r requirements.txt")
        execle(sys.executable, sys.executable, "main.py", environ)
        return
    await msg.edit(gm(chat_id, "already_newest"))


__cmds__ = ["update"]
__help__ = {
    "update": "help_update"
}
