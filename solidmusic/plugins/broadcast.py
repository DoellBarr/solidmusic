import asyncio

from pyrogram import filters

from configs import config
from solidmusic.core.client import Client, user
from pyrogram.types import Message
from solidmusic.database.chat_db import chat_db
from solidmusic.database.lang_utils import gm


@Client.on_message(filters.command("gcast") & filters.user(config.owner_id))
async def gcast_(client: Client, message: Message):
    chat_id = message.chat.id
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.text[7:]
    msg = await message.reply(
        await gm(chat_id, "process_gcast")
    )
    error = success = 0
    gcast_type = chat_db.get_chat(message.chat.id)[0]["gcast_type"]
    sender = user if gcast_type == "user" else client
    async for dialog in user.iter_dialogs():
        if dialog.chat.type in ["group", "supergroup"]:
            chat_id = dialog.chat.id
            try:
                success += 1
                await asyncio.sleep(3)
                await sender.send_message(chat_id, text)
            except Exception as e:
                print(e)
                error += 1
    return await msg.edit(
        await gm(message.chat.id, "success_gcast", [f"{success}", f"{error}"])
    )


@Client.on_message(filters.command("setgcast") & filters.user(config.owner_id))
async def set_gcast_(_, message: Message):
    chat_id = message.chat.id
    try:
        gcast_type = message.command[1]
    except IndexError:
        return await message.reply_text(await gm(chat_id, "give_me_input"))
    if gcast_type not in ["bot", "user"]:
        return await message.reply(await gm(chat_id, "invalid_gcast_type"))
    key = await chat_db.set_gcast(chat_id, gcast_type)
    return await message.reply(await gm(chat_id, key, [gcast_type]))


__cmds__ = ["gcast", "setgcast"]
__help__ = {"gcast": "help_gcast", "setgcast": "help_setgcast"}
