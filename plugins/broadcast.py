import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message

from configs import config
from core.bot import Bot
from core.clients import user
from database.lang_utils import get_message as gm
from database.chat_database import ChatDB


@Client.on_message(filters.command("gcast") & filters.user(config.OWNER_ID))
async def gcast_(client: Client, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.text[7:]
    msg = await message.reply(gm(message.chat.id, "process_gcast"))
    error = success = 0
    gcast_type = ChatDB().get_chat(message.chat.id)[0]["gcast_type"]
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
        gm(message.chat.id, "success_gcast").format(str(success), str(error))
    )


@Client.on_message(filters.command("setgcast") & filters.user(config.OWNER_ID))
async def set_gcast_(_, message: Message):
    chat_id = message.chat.id
    try:
        gcast_type = message.command[1]
    except IndexError:
        return await message.reply("Give me an input")
    if gcast_type not in ["bot", "user"]:
        return await message.reply(gm(chat_id, "invalid_gcast_type"))
    key = ChatDB().set_gcast(chat_id, gcast_type)
    return await Bot().send_message(chat_id, key, gcast_type)


__cmds__ = ["gcast", "setgcast"]
__help__ = {
    "gcast": "help_gcast",
    "setgcast": "help_setgcast"
}
