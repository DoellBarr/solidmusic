from pyrogram import Client, filters, types
from base.client_base import user
from base.bot_base import bot_client as bot
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant

from dB.lang_utils import get_message
from utils.functions.decorators import authorized_only


@Client.on_message(filters.command("userbotjoin"))
@authorized_only
async def userbot_join(client: Client, message: types.Message):
    chat_id = message.chat.id
    try:
        invite_link = await message.chat.export_invite_link()
        await user.join_chat(invite_link)
        await client.revoke_chat_invite_link(chat_id, invite_link)
        await message.chat.promote_member(
            (await user.get_me()).id,
            can_manage_voice_chats=True
        )
        return await user.send_message(chat_id, get_message(chat_id, "user_alert"))
    except UserAlreadyParticipant:
        admin = await message.chat.get_member((await user.get_me()).id)
        if not admin.can_manage_voice_chats:
            await message.chat.promote_member(
                (await user.get_me()).id,
                can_manage_voice_chats=True
            )
            return await user.send_message(chat_id, get_message(chat_id, "user_here"))
        return await user.send_message(chat_id, get_message(chat_id, "user_here"))


@Client.on_message(filters.command("userbotleave"))
@authorized_only
async def userbot_leave_(_, message: types.Message):
    chat_id = message.chat.id
    try:
        await user.leave_chat(chat_id)
        return await bot.send_message(
            message,
            "user_leave_chat",
            reply_message=True
        )
    except UserNotParticipant:
        return await bot.send_message(
            message,
            "user_already_leave_chat",
            reply_message=True
        )
