from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant

from core.clients import user
from core.bot import Bot
from database.lang_utils import get_message as gm
from functions.decorators import authorized_only


@Client.on_message(filters.command("userbotjoin"))
@authorized_only
async def userbot_join(_, message: Message):
    chat_id = message.chat.id
    try:
        invite_link = await message.chat.export_invite_link()
        if "+" in invite_link:
            link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
            await user.join_chat(f"https://t.me/joinchat/{link_hash}")
        await message.chat.promote_member(
            (await user.get_me()).id, can_manage_voice_chats=True
        )
        return await user.send_message(chat_id, gm(chat_id, "user_alert"))
    except UserAlreadyParticipant:
        admin = await message.chat.get_member((await user.get_me()).id)
        if not admin.can_manage_voice_chats:
            await message.chat.promote_member(
                (await user.get_me()).id, can_manage_voice_chats=True
            )
            return await user.send_message(chat_id, gm(chat_id, "user_here"))
        return await user.send_message(chat_id, gm(chat_id, "user_here"))


@Client.on_message(filters.command("userbotleave"))
@authorized_only
async def userbot_leave_(_, message: Message):
    chat_id = message.chat.id
    try:
        await user.leave_chat(chat_id)
        return await Bot().send_message(
            chat_id,
            "user_leave_chat",
        )
    except UserNotParticipant:
        return await Bot().send_message(
            chat_id,
            "user_already_leave_chat",
        )


__cmds__ = ["userbotjoin", "userbotleave"]
__help__ = {
    "userbotjoin": "help_userbotjoin",
    "userbotleave": "help_userbotleave"
}
