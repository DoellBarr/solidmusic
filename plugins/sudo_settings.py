from pyrogram import Client, filters, types

from database.sudo_database import SudoDB
from core.bot import Bot
from functions.decorators import authorized_only


async def process_sudo(message: types.Message, status: str):
    chat_id = message.chat.id
    reply = message.reply_to_message
    if reply:
        user_id = reply.from_user.id
        key = (
            SudoDB().add_sudo(chat_id, user_id)
            if status == "add"
            else SudoDB().del_sudo(chat_id, user_id)
        )
        return await Bot().send_message(chat_id, key)
    users = message.command[1:]
    if users:
        for user in users:
            user_ids = str(user)
            if user_ids.isnumeric():
                user_id = int(user_ids)
            elif isinstance(user_ids, types.MessageEntity) and user_ids.user:
                user_id = user_ids.user.id
            else:
                user_id = (await message.chat.get_member(user_ids)).user.id
            key = (
                SudoDB().add_sudo(chat_id, user_id)
                if status == "add"
                else SudoDB().del_sudo(chat_id, user_id)
            )
            return await Bot().send_message(chat_id, key)
    user = message.command[1]
    if user.startswith("@"):
        user_id = (await message.chat.get_member(user)).user.id
        key = (
            SudoDB().add_sudo(chat_id, user_id)
            if status == "add"
            else SudoDB().del_sudo(chat_id, user_id)
        )
        return await Bot().send_message(chat_id, key)
    if isinstance(user, types.MessageEntity) and user.user:
        user_id = user.user.id
        key = (
            SudoDB().add_sudo(chat_id, user_id)
            if status == "add"
            else SudoDB().del_sudo(chat_id, user_id)
        )
        return await Bot().send_message(chat_id, key)
    if isinstance(user, int):
        user_id = user
        key = (
            SudoDB().add_sudo(chat_id, user_id)
            if status == "add"
            else SudoDB().del_sudo(chat_id, user_id)
        )
        return await Bot().send_message(chat_id, key)


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
