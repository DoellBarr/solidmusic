from typing import Callable

from pyrogram import types, Client
from pyrogram.errors import MessageDeleteForbidden

import configs
from database.sudo_database import SudoDB
from database.chat_database import ChatDB
from core.bot import Bot
from core.clients import user

db = SudoDB()
chat_db = ChatDB()
bot = Bot()


def authorized_only(func: Callable) -> Callable:
    @check_player
    @del_cmd
    async def wrapper(client: Client, message: types.Message):
        client_user_id = (await user.get_me()).id
        user_id = message.from_user.id
        chat_id = message.chat.id
        member = await message.chat.get_member(user_id)
        if (
            member.status not in [
                "creator",
                "administrator",
            ]
            and (
                user_id not in db.get_sudos(chat_id)
                or user_id != configs.config.OWNER_ID
            )
        ):
            return await bot.send_message(
                chat_id,
                "not_allowed",
            )
        if not member.can_manage_voice_chats and member.status == "administrator":
            return await bot.send_message(chat_id, "need_privilege")
        if (
            member.status in ["creator", "administrator"]
            or user_id in db.get_sudos(chat_id)
            or user_id == client_user_id
            or user_id == configs.config.OWNER_ID
        ):
            return await func(client, message)

    return wrapper


def only_admin(func: Callable) -> Callable:
    @check_player
    @del_cmd
    async def wrapper(client: Client, message: types.Message):
        client_user_id = (await user.get_me()).id
        chat_id = message.chat.id
        user_id = message.from_user.id
        try:
            admin_only = bool(chat_db.get_chat(chat_id)[0]["only_admin"])
        except IndexError:
            ChatDB().add_chat(chat_id)
            admin_only = bool(chat_db.get_chat(chat_id)[0]["only_admin"])
        if admin_only:
            member = await message.chat.get_member(user_id)
            if member.status not in ["creator", "administrator"] or user_id != configs.config.OWNER_ID:
                return await bot.send_message(
                    chat_id,
                    "not_allowed",
                )
            if not member.can_manage_voice_chats and member.status == "administrator":
                return await bot.send_message(chat_id, "need_privilege")
            if (
                member.status in ["creator", "administrator"]
                or user_id == client_user_id
                or user_id == configs.config.OWNER_ID
            ):
                return await func(client, message)
        elif not admin_only:
            return await func(client, message)

    return wrapper


def del_cmd(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        chat_id = message.chat.id
        if message.chat.type == "private":
            return await func(client, message)
        try:
            delete_cmd = bool(chat_db.get_chat(chat_id)[0]["del_cmd_mode"])
        except IndexError:
            ChatDB().add_chat(chat_id)
            delete_cmd = bool(chat_db.get_chat(chat_id)[0]["del_cmd_mode"])
        if delete_cmd:
            try:
                await client.delete_messages(chat_id, message.message_id)
            except MessageDeleteForbidden:
                pass
            return await func(client, message)
        return await func(client, message)
    return wrapper


def check_player(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        chat_id = message.chat.id
        if message.command[0] == "player":
            return await func(client, message)
        try:
            player_mode = bool(chat_db.get_chat(chat_id)[0]["player_mode"])
        except IndexError:
            ChatDB().add_chat(chat_id)
            player_mode = bool(chat_db.get_chat(chat_id)[0]["player_mode"])
        if player_mode:
            return await func(client, message)
        return await Bot().send_message(chat_id, "player_is_nonactive")
    return wrapper
