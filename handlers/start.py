from pyrogram import filters, Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)

from base.bot_base import bot_client as bot
from dB.lang_utils import get_message as gm


def markup(chid: int, bot_username: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    gm(chid, "add_to_chat"),
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
            [InlineKeyboardButton(gm(chid, "helpbutton"), callback_data="chelp")],
            [
                InlineKeyboardButton(
                    gm(chid, "channel"), url="https://t.me/solidprojects"
                ),
                InlineKeyboardButton(
                    gm(chid, "maintainer"), url="https://t.me/talktoabdul_bot"
                ),
            ],
            [
                InlineKeyboardButton(
                    gm(chid, "source_code"),
                    url="https://github.com/DoellBarr/solidmusic_rewrite",
                )
            ],
        ]
    )


# callback


@Client.on_callback_query(filters.regex("goback"))
async def goback(_, hee: CallbackQuery):
    bot_username, _, _ = await bot.get_my()
    chid = hee.message.chat.id
    await hee.edit_message_text(
        gm(chid, "pm_greet").format(hee.message.from_user.id),
        reply_markup=markup(chid, bot_username),
    ),


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, lol: CallbackQuery):
    await lol.edit_message_text(
        f""" **Comming soon!** """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        gm(lol.message.chat.id, "backtomenu"), callback_data="goback"
                    )
                ]
            ]
        ),
    )


# message


@Client.on_message(filters.command(["start"]) & filters.private & ~filters.incoming)
async def pm_start(_, message: Message):
    bot_username, _, _ = await bot.get_my()
    chid = message.chat.id
    await bot.send_message(
        message,
        "pm_greet",
        format_key=str(message.from_user.id),
        markup=markup(chid, bot_username),
        reply_message=True,
    )


@Client.on_message(
    filters.command(["start"]) & filters.group & ~filters.edited & ~filters.channel
)
async def grp_start(_, message: Message):
    bot_username, bot_name, _ = await bot.get_my()
    mention = await bot.get_user_mention(message.chat.id, message.from_user.id)
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
