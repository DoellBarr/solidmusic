from typing import Callable

from configs import config
from solidmusic.core.client import user, Client
from pyrogram.types import Message
from solidmusic.database.chat_db import chat_db
from solidmusic.database.sudo_db import sudo_db

from pyrogram.errors import MessageDeleteForbidden


def authorized_only(func: Callable) -> Callable:
    @check_player
    @del_cmd
    async def wrapper(c: Client, m: Message):
        me_id = (await user.get_me()).id
        user_id = m.from_user.id
        chat_id = m.chat.id
        member = await m.chat.get_member(user_id)
        if (
            member.status not in {"creator", "administrator"}
            and user_id not in await sudo_db.get_sudos(chat_id)
            or user_id != config.owner_id
        ):
            return await m.reply(await gm(chat_id, "not_allowed"))
        if not member.can_manage_voice_chats and member.status == "administrator":
            return await m.reply(await gm(chat_id, "need_privilege"))
        if (
            member.status in {"creator", "administrator"}
            or user_id in await sudo_db.get_sudos(chat_id)
            or user_id == me_id
            or user_id == config.owner_id
        ):
            return await func(c, m)

    return wrapper


def only_admin(func: Callable) -> Callable:
    @check_player
    @del_cmd
    async def wrapper(c: Client, m: Message):
        me_id = (await user.get_me()).id
        user_id = m.from_user.id
        chat_id = m.chat.id
        if not await chat_db.get_chat(chat_id):
            await chat_db.add_chat(chat_id)
        admin_only = bool((await chat_db.get_chat(chat_id)).get("only_admin"))
        if not admin_only:
            return await func(c, m)
        member = await m.chat.get_member(user_id)
        if (
            member.status not in {"creator", "administrator"}
            or user_id != config.owner_id
        ):
            return await m.reply(await gm(chat_id, "not_allowed"))
        if not member.can_manage_voice_chats and member.status == "administrator":
            return await m.reply(await gm(chat_id, "need_privilege"))
        if (
            member.status in {"creator", "administrator"}
            or user_id == me_id
            or user_id == config.owner_id
        ):
            return await func(c, m)

    return wrapper


def del_cmd(func: Callable) -> Callable:
    async def wrapper(c: Client, m: Message):
        chat_id = m.chat.id
        if m.chat.type == "private":
            return await func(c, m)
        if not await chat_db.get_chat(chat_id):
            await chat_db.add_chat(chat_id)
        delete_cmd = bool((await chat_db.get_chat(chat_id)).get("del_cmd_mode"))
        if not delete_cmd:
            return await func(c, m)
        try:
            await m.delete()
        except MessageDeleteForbidden:
            pass
        return await func(c, m)

    return wrapper


def check_player(func: Callable) -> Callable:
    async def wrapper(c: Client, m: Message):
        chat_id = m.chat.id
        if m.command[0] == "player":
            return await func(c, m)
        if not await chat_db.get_chat(chat_id):
            await chat_db.add_chat(chat_id)
        player_mode = bool((await chat_db.get_chat(chat_id)).get("player_mode"))
        if not player_mode:
            return await m.reply(await gm(chat_id, "player_is_non_active"))
        return await func(c, m)

    return wrapper
