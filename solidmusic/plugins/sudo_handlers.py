from pyrogram import filters
from pyrogram.types import MessageEntity

from solidmusic.core import types
from solidmusic.core.client import Client
from solidmusic.database.sudo_db import sudo_db
from solidmusic.functions.decorators import authorized_only


async def process_sudo(message: types.Message, status: str):
    chat_id = message.chat.id
    if reply := message.reply_to_message:
        user_id = reply.from_user.id
        key = (
            await sudo_db.add_sudo(chat_id, user_id)
            if status == "add"
            else await sudo_db.del_sudo(chat_id, user_id)
        )
        return await message.reply(key)
    if users := message.command[1:]:
        for user in users:
            user_ids = str(user)
            if user_ids.isnumeric():
                user_id = int(user_ids)
            elif isinstance(user_ids, MessageEntity) and user_ids.user:
                user_id = user_ids.user.id
            else:
                user_id = (await message.chat.get_member(user_ids)).user.id
            key = (
                await sudo_db.add_sudo(chat_id, user_id)
                if status == "add"
                else await sudo_db.del_sudo(chat_id, user_id)
            )
            return await message.reply(key)
    user = message.command[1]
    if user.startswith("@"):
        user_id = (await message.chat.get_member(user)).user.id
        key = (
            await sudo_db.add_sudo(chat_id, user_id)
            if status == "add"
            else await sudo_db.del_sudo(chat_id, user_id)
        )
        return await message.reply(key)
    if isinstance(user, MessageEntity) and user.user:
        user_id = user.user.id
        key = (
            await sudo_db.add_sudo(chat_id, user_id)
            if status == "add"
            else await sudo_db.del_sudo(chat_id, user_id)
        )
        return await message.reply(key)
    if isinstance(user, int):
        user_id = user
        key = (
            await sudo_db.add_sudo(chat_id, user_id)
            if status == "add"
            else await sudo_db.del_sudo(chat_id, user_id)
        )
        return await message.reply(key)


@Client.on_message(filters.command("addsudo"))
@authorized_only
async def add_sudo_(_, message: types.Message):
    await process_sudo(message, "add")


@Client.on_message(filters.command("delsudo"))
@authorized_only
async def del_sudo_(_, message: types.Message):
    await process_sudo(message, "delete")


__cmds__ = ["addsudo", "delsudo"]
__help__ = {
    "addsudo": "help_addsudo",
    "delsudo": "help_delsudo"
}
