from pyrogram import Client, filters
from pyrogram.types import Message

from base.bot_base import bot_client as bot

from dB.database import db


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
