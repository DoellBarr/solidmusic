from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import configs
from base.player import player
from utils.call_functions import (
    prev_search,
    process_button,
    next_search,
    extract_info,
    stream_result,
)
from dB.lang_utils import get_message as gm
from dB.database import db
from base.bot_base import bot_client as bot
from utils.functions.markup_buttons import start_markup


@Client.on_callback_query(filters.regex(pattern=r"(back|next)(music|stream)\|(\d+)"))
async def _back_cb(_, cb: types.CallbackQuery):
    next_or_back = cb.matches[0].group(1)
    music_or_stream = cb.matches[0].group(2)
    user_id = int(cb.matches[0].group(3))
    if cb.message.from_user != user_id:
        return await cb.answer(gm(cb.message.chat.id, "not_allowed"), show_alert=True)
    yt_btn = process_button(cb.message.from_user.id, music_or_stream)
    if next_or_back == "next":
        next_search(cb.message.chat.id)
        btn = [
            InlineKeyboardButton("⬅", f"back{music_or_stream}"),
            InlineKeyboardButton("🗑", "close"),
            InlineKeyboardButton("➡", f"next{music_or_stream}"),
        ]
    else:
        prev_search(cb.message.chat.id)
        btn = [
            InlineKeyboardButton("🗑", "close"),
            InlineKeyboardButton("➡", f"next{music_or_stream}"),
        ]
    res = extract_info(cb.message.chat.id, stream_result)
    await cb.edit_message_text(
        res,
        reply_markup=InlineKeyboardMarkup(
            [
                yt_btn[0],
                yt_btn[1],
                btn,
            ]
        ),
    )


@Client.on_callback_query(filters.regex(pattern=r"((stream|music) ((\d)\|(\d+)))"))
async def stream_or_play(_, cb: types.CallbackQuery):
    chat_id = cb.message.chat.id
    match = cb.matches[0].group
    stream_type = match(2)
    index = int(match(4))
    user_id = match(5)
    result = stream_result[chat_id][0][index]
    res = {
        "user_id": user_id,
        "title": result["title"],
        "duration": result["duration"],
        "yt_id": result["yt_id"],
        "yt_url": result["yt_url"],
        "stream_type": stream_type,
    }
    await player.play_or_stream(cb, res)


@Client.on_callback_query(filters.regex(pattern=r"(close)(\|(\d+))?"))
async def close_button_(_, cb: types.CallbackQuery):
    match = cb.matches[0].group
    try:
        user_id = int(match(3))
    except TypeError:
        user_id = None
    if not user_id:
        return await cb.message.delete()
    if cb.from_user.id != user_id:
        return await cb.answer(gm(cb.message.chat.id, "not_for_you"), show_alert=True)
    member = await cb.message.chat.get_member(cb.from_user.id)
    if member.status in ["creator", "administrator"]:
        return await cb.message.delete()
    return await cb.message.delete()


@Client.on_callback_query(filters.regex("goback"))
async def goback(_, hee: types.CallbackQuery):
    bot_username, _, _ = await bot.get_my()
    chid = hee.message.chat.id
    await hee.edit_message_text(
        gm(chid, "pm_greet").format(hee.message.from_user.mention),
        reply_markup=start_markup(chid, bot_username),
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, lol: types.CallbackQuery):
    return await lol.edit_message_text(
        gm(lol.message.chat.id, "helpmusic"),
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


@Client.on_callback_query(filters.regex("set_lang_(.*)"))
async def cb_change_lang(_, cb: types.CallbackQuery):
    lang = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    db.set_chat_lang(chat_id, lang)
    await cb.message.edit(
        gm(chat_id, "lang_changed"),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(gm(chat_id, "channel"), url=configs.config.CHANNEL)
                ]
            ]
        )
    )
