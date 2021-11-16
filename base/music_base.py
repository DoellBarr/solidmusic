from asyncio import sleep
from typing import Union

from pyrogram import types
from pyrogram.errors import FloodWait
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped, AudioParameters

from dB.database import db
from dB.lang_utils import get_message as gm
from utils.functions.yt_utils import get_audio_direct_link
from .call_base import CallBase

add_chat = db.add_chat


class MusicPlayer(CallBase):
    async def _set_play(
        self,
        chat_id: int,
        user_id: int,
        audio_url: str,
        title: str,
        duration: Union[str, int],
        yt_url: str,
        yt_id: str,
    ):
        playlist = self.playlist
        call = self.call
        playlist[chat_id] = [
            {
                "user_id": user_id,
                "title": title,
                "duration": duration,
                "yt_url": yt_url,
                "yt_id": yt_id,
                "stream_type": "music",
            }
        ]
        quality: str = db.get_chat(chat_id)[0]["video_quality"]
        if quality.lower() not in ["low", "medium", "high"]:
            raise KeyError("Invalid quality.")
        if quality.lower() == "low":
            audio_quality = AudioParameters(bitrate=24000)
        else:
            audio_quality = AudioParameters(bitrate=48000)
        try:
            await call.join_group_call(
                chat_id,
                AudioPiped(audio_url, audio_quality),
                stream_type=StreamType().local_stream,
            )
        except NoActiveGroupCall:
            await self.create_call(chat_id)
            await call.join_group_call(
                chat_id,
                AudioPiped(audio_url, audio_quality),
                stream_type=StreamType().local_stream,
            )

    async def _set_playing(
        self,
        chat_id: int,
        user_id: int,
        audio_url: str,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
        messy: types.Message,
    ):
        bot_username, _, _ = await self.bot.get_my()
        mention = await self.bot.get_user_mention(chat_id, user_id)
        await self._set_play(
            chat_id, user_id, audio_url, title, duration, yt_url, yt_id
        )
        await messy.edit(
            f"""
{gm(chat_id, 'now_streaming')}
📌 {gm(chat_id, 'yt_title')}: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})
🕰 {gm(chat_id, 'duration')}: {duration}
✨ {gm(chat_id, 'req_by')}: {mention}
📽 {gm(chat_id, 'stream_type_title')}: {gm(chat_id, 'stream_type_music')}
""",
            disable_web_page_preview=True,
        )

    async def play(
        self,
        cb: types.CallbackQuery,
        user_id: int,
        title: str,
        duration: Union[str, int],
        yt_url: str,
        yt_id: str,
    ):
        playlist = self.playlist
        chat_id = cb.message.chat.id
        if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
            self.extend_playlist(
                user_id, chat_id, title, duration, yt_url, yt_id, "music"
            )
            mess = await cb.edit_message_text(gm(chat_id, "track_queued"))
            await sleep(5)
            return await mess.delete()
        messy = await cb.edit_message_text(gm(chat_id, "process"))
        audio_quality = db.get_chat(chat_id)[0]["video_quality"]
        audio_url = get_audio_direct_link(yt_url, audio_quality)
        try:
            await self._set_playing(
                chat_id, user_id, audio_url, title, duration, yt_url, yt_id, messy
            )
        except FloodWait as e:
            await messy.edit(gm(chat_id, "error_flood").format(e.x))
            await sleep(e.x)
            await self._set_playing(
                chat_id, user_id, audio_url, title, duration, yt_url, yt_id, messy
            )
