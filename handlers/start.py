from pyrogram import filters, Client
from pyrogram.methods.messages import send_message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from base.client_base import bot
from dB.lang_utils import get_message as gm

#callback

@Client.on_callback_query(filters.regex("goback"))
async def goback(_, hee: CallbackQuery):
    BOT_USERNAME = (await bot.get_me()).username
    chid = hee.message.chat.id
    await hee.edit_message_text(gm(chid, "pm_greet").format(hee.message.from_user.id),
    reply_markup = InlineKeyboardMarkup(
        [   [
            InlineKeyboardButton(
                gm(chid, "add_to_chat"), url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],[
            InlineKeyboardButton(
                gm(chid, "helpbutton"), callback_data="chelp")
            ],[
            InlineKeyboardButton(
                gm(chid, "channel"), url=f"https://t.me/solidprojects"),
            InlineKeyboardButton(
                gm(chid,"maintainer"), url=f"https://t.me/talktoabdul_bot")
            ],[
            InlineKeyboardButton(
                gm(chid, "source_code"),url=f"https://github.com/DoellBarr/solidmusic_rewrite")
            ]
        ])
    )

@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, lol: CallbackQuery):
    await lol.edit_message_text(
    f""" **Comming soon!** """,

    reply_markup = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton(gm(lol.message.chat.id, "backtomenu"), callback_data="goback")
    ]]
    ))

#message

@Client.on_message(filters.command(["start"]) &filters.private & ~filters.incoming)
async def pm_start(_, message: Message):
    BOT_USERNAME = (await bot.get_me()).username
    chid = message.chat.id
    await send_message(gm(chid, "pm_greet").format(message.from_user.id),
    reply_markup = InlineKeyboardMarkup(
        [   [
            InlineKeyboardButton(
                gm(chid, "add_to_chat"), url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],[
            InlineKeyboardButton(
                gm(chid, "helpbutton"), callback_data="chelp")
            ],[
            InlineKeyboardButton(
                gm(chid, "channel"), url=f"https://t.me/solidprojects"),
            InlineKeyboardButton(
                gm(chid,"maintainer"), url=f"https://t.me/talktoabdul_bot")
            ],[
            InlineKeyboardButton(
                gm(chid, "source_code"),url=f"https://github.com/DoellBarr/solidmusic_rewrite"
            )
            ]
        ])
    )
 
@Client.on_message(filters.command(["start"]) & filters.group & ~filters.edited & ~filters.channel)
async def grp_start(_, message: Message):
    first_name = (await bot.get_me()).first_name
    BOT_USERNAME = (await bot.get_me()).username
    bot_name = f"{first_name if first_name.endswith in ['bot', 'Bot', 'BOT'] else 'bot'}"

    await message.reply_text(gm(message.chat.id, "chat_greet").format(message.from_user.mention, bot_name),
    reply_markup=InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
            gm(message.chat.id, "group_buttn"), url=f"https://t.me/{BOT_USERNAME}?start")
        ]]
    ))
