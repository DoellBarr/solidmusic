from pyrogram import Client, filters, types
from dB.database import db
from base.bot_base import bot_client as bot


@Client.on_message(filters.command("addsudo"))
async def add_sudo_(_, message: types.Message):
    chat_id = message.chat.id
    reply = message.reply_to_message
    if reply:
        user_id = reply.from_user.id
        toxt = db.add_sudo(chat_id, user_id)
        return await bot.send_message(
            message,
            toxt,
            reply_message=True
        )
    user_id = int(message.command[1])
    toxt = db.add_sudo(chat_id, user_id)
    return await bot.send_message(
        message,
        toxt,
        str(user_id),
        reply_message=True
    )


@Client.on_message(filters.command("delsudo"))
async def del_sudo_(_, message: types.Message):
    chat_id = message.chat.id
    reply = message.reply_to_message
    if reply:
        user_id = reply.from_user.id
        toxt = db.del_sudo(chat_id, user_id)
        return await bot.send_message(
            message,
            toxt,
            reply_message=True
        )
    user_id = int(message.command[1])
    toxt = db.del_sudo(chat_id, user_id)
    return await bot.send_message(
        message,
        toxt,
        str(user_id),
        reply_message=True
    )
