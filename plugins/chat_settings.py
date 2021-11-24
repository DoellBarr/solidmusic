from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup as MarkupKeyboard, InlineKeyboardButton as ButtonKeyboard
from core.bot import Bot
from core.clients import user
from configs import config
from database.chat_database import ChatDB
from functions.decorators import authorized_only


@Client.on_message(filters.new_chat_members)
async def new_member_(client: Client, message: Message):
    assistant_username = (await user.get_me()).username
    bot_id = (await client.get_me()).id
    for member in message.new_chat_members:
        if member.id == bot_id:
            ChatDB().add_chat(message.chat.id)
            return await message.reply(
                "Hi, english is my default language.\n"
                "make me as admin in here with all permissions except anonymous admin\n"
                "btw, thanks for inviting me to here, to use me, please use /userbotjoin command first.\n"
                "and for changing language, tap /lang to see all language that supported for me, "
                "don't forget to subscribe our channel.",
                reply_markup=MarkupKeyboard(
                    [
                        [
                            ButtonKeyboard("Channel", url=config.CHANNEL_LINK),
                            ButtonKeyboard("Support", url=config.GROUP_LINK)
                        ],
                        [
                            ButtonKeyboard("Assistant", url=f"https://t.me/{assistant_username}")
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
            ChatDB().add_chat(int(chat_id), lang)
        return await Bot().send_message(message.chat.id, "success_add_chats")
    add_status = ChatDB().add_chat(message.chat.id, lang)
    return await Bot().send_message(message.chat.id, add_status)


@Client.on_message(filters.command("delchat"))
@authorized_only
async def del_chat_(_, message: Message):
    cmds = message.command[1:]
    if cmds:
        for chat_id in cmds:
            ChatDB().del_chat(int(chat_id))
        return await Bot().send_message(message.chat.id, "success_del_chats")
    del_status = ChatDB().del_chat(message.chat.id)
    return await Bot().send_message(message.chat.id, del_status)


@Client.on_message(filters.command("setadmin"))
@authorized_only
async def set_admin_(_, message: Message):
    try:
        cmd = message.command[1].lower()
    except IndexError:
        cmd = ""
    if cmd not in ["yes", "true", "on", "no", "false", "off"]:
        return await Bot().send_message(message.chat.id, "invalid_selection")
    if cmd in ["yes", "true", "on"]:
        only_admin = True
    else:
        only_admin = False
    admin_set = ChatDB().set_admin(message.chat.id, only_admin)
    if admin_set and only_admin:
        return await Bot().send_message(
            message.chat.id, "stream_only_can_use_by_admin"
        )
    if admin_set and not only_admin:
        return await Bot().send_message(
            message.chat.id, "stream_can_use_by_member"
        )


@Client.on_message(filters.command("setquality"))
@authorized_only
async def set_quality_(_, message: Message):
    try:
        cmd = message.command[1].lower()
    except IndexError:
        cmd = ""
    if cmd:
        if cmd not in ["low", "medium", "high"]:
            return await Bot().send_message(message.chat.id, "invalid_selection")
        key = ChatDB().set_quality(message.chat.id, cmd)
        return await Bot().send_message(message.chat.id, key, cmd)
