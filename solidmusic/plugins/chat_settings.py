from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton as ButtonKeyboard,
    InlineKeyboardMarkup as MarkupKeyboard,
)

from configs import config
from solidmusic.core.client import Client, user
from pyrogram.types import Message
from solidmusic.database.chat_db import chat_db
from solidmusic.database.lang_utils import gm
from solidmusic.functions.decorators import authorized_only


def check_cmd(message: Message):
    return message.command[1].lower() if len(message.command) > 1 else ""


@Client.on_message(filters.new_chat_members)
async def new_member_(client: Client, message: Message):
    assistant_username = (await user.get_me()).username
    bot_id = (await client.get_me()).id
    for member in message.new_chat_members:
        if member.id == bot_id:
            await chat_db.add_chat(message.chat.id)
            return await message.reply(
                "Hi), english is my default language.\n"
                "make me as admin in here with all permissions except anonymous admin\n"
                "btw, thanks for inviting me to here, to use me, please use /userbotjoin command first.\n"
                "and for changing language, tap /lang to see all language that supported for me, "
                "don't forget to subscribe our channel.",
                reply_markup=MarkupKeyboard(
                    [
                        [
                            ButtonKeyboard("Channel", url=config.channel_link),
                            ButtonKeyboard("Support", url=config.group_link),
                        ],
                        [
                            ButtonKeyboard(
                                "Assistant", url=f"https://t.me/{assistant_username}"
                            )
                        ],
                    ]
                ),
            )


@Client.on_message(filters.command("addchat"))
@authorized_only
async def add_chat_(_, message: Message):
    chat_id = message.chat.id
    try:
        lang = (await message.chat.get_member(message.from_user.id)).user.language_code
    except (AttributeError, ValueError):
        lang = "en"
    if cmds := message.command[1:]:
        for ch_id in cmds:
            await chat_db.add_chat(int(ch_id), lang)
        return await message.reply(await gm(chat_id, "success_add_chats"))
    add_status = await chat_db.add_chat(message.chat.id, lang)
    return await message.reply(await gm(chat_id, add_status))


@Client.on_message(filters.command("delchat"))
@authorized_only
async def del_chat_(_, message: Message):
    chat_id = message.chat.id
    if cmds := message.command[1:]:
        for ch_id in cmds:
            await chat_db.del_chat(int(ch_id))
        return await message.reply(await gm(chat_id, "success_delete_chats"))
    del_status = await chat_db.del_chat(message.chat.id)
    return await message.reply(await gm(chat_id, del_status))


@Client.on_message(filters.command("setadmin"))
@authorized_only
async def set_admin_(_, message: Message):
    cmd = check_cmd(message)
    chat_id = message.chat.id
    if cmd not in ["yes", "true", "on", "no", "false", "off"]:
        return await message.reply(await gm(chat_id, "invalid_command_selection"))
    only_admin = bool(cmd in ["yes", "true", "on"])
    admin_set = await chat_db.set_admin_mode(message.chat.id, only_admin)
    return await message.reply(await gm(chat_id, admin_set))


@Client.on_message(filters.command("setquality"))
@authorized_only
async def set_quality_(_, message: Message):
    chat_id = message.chat.id
    if cmd := check_cmd(message):
        if cmd not in ["low", "medium", "high"]:
            return await message.reply(await gm(chat_id, "invalid_quality_selection"))
        key = await chat_db.set_quality(message.chat.id, cmd)
        return await message.reply(await gm(chat_id, key, [cmd]))


@Client.on_message(filters.command("delcmd"))
@authorized_only
async def set_del_cmd_(_, message: Message):
    cmd = check_cmd(message)
    chat_id = message.chat.id
    if cmd not in ["on", "yes", "true", "off", "no", "false"]:
        return await message.reply(await gm(chat_id, "invalid_command_selection"))
    del_cmd = bool(cmd in ["on", "yes", "true"])
    key = await chat_db.set_del_cmd_mode(message.chat.id, del_cmd)
    return await message.reply(await gm(chat_id, key, [cmd]))


@Client.on_message(filters.command("player") & filters.group)
@authorized_only
async def set_player_mode(_, message: Message):
    chat_id = message.chat.id
    cmd = check_cmd(message)
    set_play_mode = bool(cmd in ["on", "yes", "true"])
    key = await chat_db.set_player_mode(chat_id, set_play_mode)
    return await message.reply(await gm(chat_id, key, [cmd]))


@Client.on_message(filters.command("setduration") & filters.group)
@authorized_only
async def set_duration_limit(_, m: Message):
    chat_id = m.chat.id
    duration = int(m.command[1])
    key = await chat_db.set_duration_limit(chat_id, duration)
    return await m.reply(await gm(chat_id, key, [str(duration)]))


__cmds__ = [
    "addchat",
    "delchat",
    "setadmin",
    "setquality",
    "delcmd",
    "reloaddb",
    "player",
    "setduration",
]
__help__ = {
    "addchat": "help_addchat",
    "delchat": "help_delchat",
    "setadmin": "help_setadmin",
    "setquality": "help_setquality",
    "delcmd": "help_delcmd",
    "reloaddb": "help_reloaddb",
    "player": "help_player",
    "setduration": "help_setduration",
}
