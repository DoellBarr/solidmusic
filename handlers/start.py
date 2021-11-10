from pyrogram import filters, Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)

from base.bot_base import bot_client as bot
from dB.lang_utils import get_message as gm
from configs import config
from utils.functions.markup_buttons import start_markup


@Client.on_message(filters.command("start"))
async def pm_start(_, message: Message):
    bot_username, bot_name, _ = await bot.get_my()
    chid = message.chat.id
    mention = await bot.get_user_mention(message.chat.id, message.from_user.id)
    if message.chat.type == "private":
        return await bot.send_message(
            message,
            "pm_greet",
            format_key=str(mention),
            markup=start_markup(chid, bot_username),
            reply_message=True,
        )
    if message.chat.type in ["group", "supergroup"]:
        await bot.send_message(
            message,
            "chat_greet",
            (mention, bot_name),
            reply_message=True,
            markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            gm(message.chat.id, "group_buttn"),
                            url=f"https://t.me/{bot_username}?start",
                        )
                    ]
                ]
            ),
        )
