import asyncio

from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, Message

from base.bot_base import bot_client as bot
from base.client_base import user

from dB.database import db
from dB.lang_utils import get_message as gm


@Client.on_chat_member_updated(filters.group)
async def chat_member_update_(_, message: ChatMemberUpdated):
    _, _, bot_id = await bot.get_my()
    member = message.new_chat_member.user
    member_id = member.id
    try:
        lang = member.language_code
    except AttributeError:
        lang = "en"
    if member_id == bot_id:
        return db.add_chat(message.chat.id, lang)
    return


@Client.on_message(filters.left_chat_member)
async def on_bot_left_(_, message: Message):
    _, _, bot_id = await bot.get_my()
    chat_id = message.chat.id
    member_id = message.left_chat_member.id
    if member_id == bot_id:
        db.del_chat(chat_id)
        await user.send_message(chat_id, gm(chat_id, "bot_leave_from_chat"))
        await asyncio.sleep(3)
        return await user.leave_chat(chat_id)


@Client.on_message(filters.command("addchat"))
async def add_chat_(_, message: Message):
    try:
        lang = (await message.chat.get_member(message.from_user.id)).user.language_code
    except (AttributeError, ValueError):
        lang = "en"
    cmds = message.command[1:]
    if cmds:
        for chat_id in cmds:
            db.add_chat(chat_id, lang)
        return await bot.send_message(message, "success_add_chats", reply_message=True)
    db.add_chat(message.chat.id, lang)
    return await bot.send_message(message, "success_add_chat", reply_message=True)


@Client.on_message(filters.command("delchat"))
async def del_chat_(_, message: Message):
    cmds = message.command[1:]
    if cmds:
        for chat_id in cmds:
            db.del_chat(chat_id)
        return await bot.send_message(message, "success_del_chats", reply_message=True)
    db.del_chat(message.chat.id)
    return await bot.send_message(message, "success_del_chat", reply_message=True)


@Client.on_message(filters.command("setquality"))
async def set_vid_quality(_, message: Message):
    quality = "".join(message.command[1]).lower()
    if quality not in ["low", "medium", "high"]:
        return await bot.send_message(
            message,
            "quality_invalid",
            reply_message=True
        )
    db.set_video_quality(message.chat.id, quality)
    return await bot.send_message(
        message,
        "success_change_quality",
        quality,
        reply_message=True
    )
