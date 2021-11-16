from typing import Callable

from pyrogram import types, Client
from dB.database import db
from base.bot_base import bot_client as bot


def authorized_only(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        member = await message.chat.get_member(user_id)
        if member.status not in ["creator", "administrator"] and user_id not in db.get_sudos(chat_id):
            return await bot.send_message(
                message,
                "not_allowed",
                reply_message=True
            )
        if not member.can_manage_voice_chats and member.status == "administrator":
            return await bot.send_message(
                message,
                "need_privilege",
                reply_message=True
            )
        if member.status in ["creator", "administrator"] or user_id in db.get_sudos(chat_id):
            return await func(client, message)
        if message.chat.type == "private":
            return await func(client, message)

    return wrapper


def only_admin(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        only_admins = db.get_chat(message.chat.id)[0]["only_admin"]
        adminun = bool(only_admins)
        if adminun:
            member = await message.chat.get_member(message.from_user.id)
            if member.status not in ["creator", "administrator"]:
                return await bot.send_message(
                    message,
                    "not_allowed",
                    reply_message=True
                )
            if not member.can_manage_voice_chats and member.status == "administrator":
                return await bot.send_message(
                    message,
                    "need_privilege",
                    reply_message=True
                )
            if member.status in ["creator", "administrator"]:
                return await func(client, message)
        if not adminun:
            return await func(client, message)
    return wrapper
