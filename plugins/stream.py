from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.player import player
from database.lang_utils import get_message
from functions.youtube_utils import (
    extract_info,
    stream_result,
    yt_search,
)
from functions.decorators import only_admin
from functions.markup_button import process_button


def extract_all(query: str, chat_id: int, user_id: int, status: str):
    yt_btn = process_button(user_id, status)
    yt_search(chat_id, query)
    result = extract_info(chat_id, stream_result)
    return result, yt_btn


@Client.on_message(filters.command("play") & filters.group)
@only_admin
async def play_(_, message: types.Message):
    reply = message.reply_to_message
    user_id = message.from_user.id
    chat_id = message.chat.id
    if reply:
        return await player.local_music(user_id, reply)
    command = message.command
    if len(command) == 1:
        return await message.reply(get_message(chat_id, "wrong_play_vplay_input"))
    query = " ".join(command[1:])
    status = "music"
    result, yt_btn = extract_all(query, chat_id, user_id, status)
    await message.reply(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                yt_btn[0],
                yt_btn[1],
                [
                    InlineKeyboardButton("🗑", f"close|{user_id}"),
                    InlineKeyboardButton("➡", f"nextmusic|{user_id}"),
                ],
            ],
        ),
    )


@Client.on_message(filters.command("vplay") & filters.group)
@only_admin
async def vplay_(_, message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    reply = message.reply_to_message
    if reply:
        return await player.local_video(user_id, reply)
    commands = message.command
    if len(commands) == 1:
        return await message.reply(get_message(chat_id, "wrong_play_vplay_input"))
    query = " ".join(commands[1:])
    status = "video"
    result, yt_btn = extract_all(query, chat_id, user_id, status)
    await message.reply(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                yt_btn[0],
                yt_btn[1],
                [
                    InlineKeyboardButton("🗑", f"close|{user_id}"),
                    InlineKeyboardButton("➡", f"nextvideo|{user_id}"),
                ],
            ]
        ),
    )


__cmds__ = ["play", "vplay"]
__help__ = {
    "play": "help_play",
    "vplay": "help_vplay"
}
