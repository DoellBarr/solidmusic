from pyrogram import Client, filters, types
from dB.database import db
from base.bot_base import bot_client as bot
from utils.functions.decorators import authorized_only


@Client.on_message(filters.command("addsudo"))
@authorized_only
async def add_sudo_(_, message: types.Message):
    chat_id = message.chat.id
    reply = message.reply_to_message
    user = message.command[1]
    if reply:
        user_id = reply.from_user.id
        toxt = db.add_sudo(chat_id, user_id)
        return await bot.send_message(message, toxt, reply_message=True)
    if user.startswith("@"):
        user_id = (await message.chat.get_member(user)).user.id
        toxt = db.add_sudo(chat_id, user_id)
        return await bot.send_message(message, toxt, user, reply_message=True)
    user_id = int(user)
    toxt = db.add_sudo(chat_id, user_id)
    return await bot.send_message(message, toxt, str(user_id), reply_message=True)


@Client.on_message(filters.command("delsudo"))
@authorized_only
async def del_sudo_(_, message: types.Message):
    chat_id = message.chat.id
    reply = message.reply_to_message
    user = message.command[1]
    if reply:
        user_id = reply.from_user.id
        toxt = db.del_sudo(chat_id, user_id)
        return await bot.send_message(message, toxt, reply_message=True)
    if user.startswith("@"):
        user_id = (await message.chat.get_member(user)).user.id
        toxt = db.del_sudo(chat_id, user_id)
        return await bot.send_message(message, toxt, user, reply_message=True)
    user_id = int(user)
    toxt = db.del_sudo(chat_id, user_id)
    return await bot.send_message(message, toxt, str(user_id), reply_message=True)
