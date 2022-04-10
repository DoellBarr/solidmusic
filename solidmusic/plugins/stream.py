from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram import types
from solidmusic.core.client import Client
from solidmusic.core.player import player
from solidmusic.database.lang_utils import gm
from solidmusic.functions.decorators import only_admin
from solidmusic.functions.markup_button import process_button
from solidmusic.functions.yt_utils import yt_search, extract_info, stream_result


async def extract_all(query: str, chat_id: int, user_id: int, status: str):
    yt_btn = process_button(user_id, status)
    await yt_search(chat_id, query)
    result = await extract_info(chat_id, stream_result)
    return result, yt_btn


@Client.on_message(filters.command("play") & filters.group)
@only_admin
async def play_(_, message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if reply := message.reply_to_message:
        return await player.local_music(user_id, reply)
    command = message.command
    if len(command) == 1:
        return await message.reply(await gm(chat_id, "wrong_play_vplay_input"))
    query = " ".join(command[1:])
    status = "music"
    result, yt_btn = await extract_all(query, chat_id, user_id, status)
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
        disable_web_page_preview=True,
        parse_mode="Markdown"
    )


@Client.on_message(filters.command("vplay") & filters.group)
@only_admin
async def vplay_(_, message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if reply := message.reply_to_message:
        return await player.local_video(user_id, reply)
    commands = message.command
    if len(commands) == 1:
        return await message.reply(await gm(chat_id, "wrong_play_vplay_input"))
    query = " ".join(commands[1:])
    status = "video"
    result, yt_btn = await extract_all(query, chat_id, user_id, status)
    await message.reply(
        await gm(chat_id, result),
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
__help__ = {"play": "help_play", "vplay": "help_vplay"}
