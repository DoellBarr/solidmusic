from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from base.bot_base import bot_client as bot
from base.client_base import user
from configs import config
from dB.database import db
from utils.functions.decorators import authorized_only


@Client.on_message(filters.new_chat_members)
async def new_member_(client: Client, message: Message):
    assistant_username = (await user.get_me()).username
    bot_id = (await client.get_me()).id
    for member in message.new_chat_members:
        if member.id == bot_id:
            db.add_chat(message.chat.id)
            return await message.reply(
                "Hi, english is my default language.\n"
                "make me as admin in here with all permissions except anonymous admin\n"
                "btw, thanks for inviting me to here, to use me, please use /userbotjoin command first.\n"
                "and for changing language, tap /lang to see all language that supported for me, "
                "don't forget to subscribe our channel.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Channel", url=config.CHANNEL),
                            InlineKeyboardButton("Developer", url="https://t.me/talktoabdul_bot"),
                        ],
                        [
                            InlineKeyboardButton("Assistant", url=f"https://t.me/{assistant_username}")
                        ]
                    ]
                )
            )


@Client.on_message(filters.command("addchat"))
@authorized_only
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
    add_status = db.add_chat(message.chat.id, lang)
    if add_status:
        return await bot.send_message(message, "success_add_chat", reply_message=True)
    return await bot.send_message(message, "already_added_chat", reply_message=True)


@Client.on_message(filters.command("delchat"))
@authorized_only
async def del_chat_(_, message: Message):
    cmds = message.command[1:]
    if cmds:
        for chat_id in cmds:
            db.del_chat(chat_id)
        return await bot.send_message(message, "success_del_chats", reply_message=True)
    del_status = db.del_chat(message.chat.id)
    if del_status:
        return await bot.send_message(message, "success_del_chat", reply_message=True)
    return await bot.send_message(message, "already_deleted_chat")


@Client.on_message(filters.command("setquality"))
@authorized_only
async def set_vid_quality(_, message: Message):
    quality = "".join(message.command[1]).lower()
    if quality not in ["low", "medium", "high"]:
        return await bot.send_message(message, "quality_invalid", reply_message=True)
    db.set_video_quality(message.chat.id, quality)
    return await bot.send_message(
        message, "success_change_quality", quality, reply_message=True
    )


@Client.on_message(filters.command("setadmin"))
@authorized_only
async def set_only_admin_(_, message: Message):
    try:
        cmd = message.command[1].lower()
    except IndexError:
        cmd = ""
    if cmd not in ["yes", "true", "no", "false"]:
        return await bot.send_message(message, "invalid_selection", reply_message=True)
    only_admin: bool = False
    if cmd in ["yes", "true"]:
        only_admin = True
    elif cmd in ["no", "false"]:
        only_admin = False
    pak = db.set_only_admin_stream(message.chat.id, only_admin)
    if pak and only_admin:
        return await bot.send_message(
            message, "stream_only_can_use_by_admin", reply_message=True
        )
    if pak and not only_admin:
        return await bot.send_message(
            message, "stream_can_use_by_member"
        )
