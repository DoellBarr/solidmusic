from typing import Callable

from pyrogram import types, Client
from dB.database import db
from base.bot_base import bot_client as bot


def authorized_only(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        if message.from_user.id in db.get_sudos(message.chat.id):
            return await func(client, message)
        admins = await message.chat.get_members(filter="administrators")
        for admin in admins:
            if not admin.can_manage_voice_chats:
                return await bot.send_message(
                    message,
                    "need_privilege",
                    reply_message=True
                )
            return await func(client, message)
        if not admins or (message.from_user.id not in db.get_sudos(message.chat.id)):
            return await bot.send_message(
                message,
                "not_allowed",
                reply_message=True
            )
    return wrapper
