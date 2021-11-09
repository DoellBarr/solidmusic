from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from base.player import player
from utils.call_functions import (
    prev_search,
    process_button,
    next_search,
    extract_info,
    stream_result,
)
from dB.lang_utils import get_message as gm


@Client.on_callback_query(filters.regex(pattern=r"(back|next)(music|stream)"))
async def _back_cb(_, cb: types.CallbackQuery):
    next_or_back = cb.matches[0].group(1)
    music_or_stream = cb.matches[0].group(2)
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


@Client.on_callback_query(filters.regex(pattern=r"(close)\|(\d+)"))
async def close_button_(_, cb: types.CallbackQuery):
    match = cb.matches[0].group
    user_id = int(match(1))
    if cb.from_user.id != user_id:
        return await cb.answer(gm(cb.message.chat.id, "not_for_you"), show_alert=True)
    return await cb.message.delete()
