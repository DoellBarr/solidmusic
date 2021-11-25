from typing import Callable

from pyrogram import types, Client
from database.sudo_database import SudoDB
from database.chat_database import ChatDB
from core.bot import Bot
from core.clients import user
db = SudoDB()
chat_db = ChatDB()
bot = Bot()


def authorized_only(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        client_user_id = (await user.get_me()).id
        user_id = message.from_user.id
        chat_id = message.chat.id
        member = await message.chat.get_member(user_id)
        if member.status not in ["creator", "administrator"] and user_id not in db.get_sudos(chat_id):
            return await bot.send_message(
                chat_id,
                "not_allowed",
            )
        if not member.can_manage_voice_chats and member.status == "administrator":
            return await bot.send_message(
                chat_id,
                "need_privilege"
            )
        if (
            member.status in ["creator", "administrator"]
            or user_id in db.get_sudos(chat_id)
            or user_id == client_user_id
        ):
            return await func(client, message)

    return wrapper


def only_admin(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        client_user_id = (await user.get_me()).id
        chat_id = message.chat.id
        user_id = message.from_user.id
        admin_only = bool(chat_db.get_chat(chat_id)[0]["only_admin"])
        if admin_only:
            member = await message.chat.get_member(user_id)
            if member.status not in ["creator", "administrator"]:
                return await bot.send_message(
                    chat_id,
                    "not_allowed",
                )
            if not member.can_manage_voice_chats and member.status == "administrator":
                return await bot.send_message(
                    chat_id,
                    "need_privilege"
                )
            if member.status in ["creator", "administrator"] or user_id == client_user_id:
                return await func(client, message)
        if not admin_only:
            return await func(client, message)
    return wrapper
