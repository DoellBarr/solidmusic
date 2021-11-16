from typing import Union
from asyncio import sleep

from pyrogram import types
from pyrogram.errors import FloodWait
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    MediumQualityVideo,
    LowQualityVideo,
    LowQualityAudio,
    MediumQualityAudio,
)


from dB.database import db
from dB.lang_utils import get_message as gm
from utils.functions.yt_utils import get_video_direct_link

from .call_base import CallBase

add_chat = db.add_chat


class VideoPlayer(CallBase):
    async def _set_stream(
        self,
        chat_id: int,
        user_id: int,
        video_direct_link: str,
        quality: str,
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
                "stream_type": "stream",
            }
        ]
        if quality == "low":
            video_quality = LowQualityVideo()
            audio_quality = LowQualityAudio()
        elif quality == "medium":
            video_quality = MediumQualityVideo()
            audio_quality = MediumQualityAudio()
        else:
            video_quality = HighQualityVideo()
            audio_quality = HighQualityAudio()
        try:
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(video_direct_link, audio_quality, video_quality),
                stream_type=StreamType().local_stream,
            )
        except NoActiveGroupCall:
            await self.create_call(chat_id)
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(video_direct_link, audio_quality, video_quality),
                stream_type=StreamType().local_stream,
            )

    async def _set_streaming(
        self,
        chat_id: int,
        user_id: int,
        video_url: str,
        quality: str,
        title: str,
        duration: Union[str, int],
        yt_url: str,
        yt_id: str,
        messy: types.Message,
    ):
        mention = await self.bot.get_user_mention(chat_id, user_id)
        bot_username, _, _ = await self.bot.get_my()
        await self._set_stream(
            chat_id, user_id, video_url, quality, title, duration, yt_url, yt_id
        )
        return await messy.edit(
            f"""
{gm(chat_id, 'now_streaming')}
📌 {gm(chat_id, 'yt_title')}: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})
🕰 {gm(chat_id, 'duration')}: {duration}
✨ {gm(chat_id, 'req_by')}: {mention}
📽 {gm(chat_id, 'stream_type_title')}: {gm(chat_id, 'stream_type_video')}
            """,
            disable_web_page_preview=True,
        )

    async def stream(
        self,
        cb: types.CallbackQuery,
        user_id: int,
        title: str,
        duration: Union[str, int],
        yt_url: str,
        yt_id: str,
        quality: str,
    ):
        playlist = self.playlist
        chat_id = cb.message.chat.id
        if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
            self.extend_playlist(
                user_id, chat_id, title, duration, yt_url, yt_id, "stream"
            )
            mess = await cb.edit_message_text(gm(chat_id, "track_queued"))
            await sleep(5)
            return await mess.delete()
        messy = await cb.edit_message_text(gm(chat_id, "process"))
        video_url = get_video_direct_link(yt_url, quality)
        try:
            await self._set_streaming(
                chat_id,
                user_id,
                video_url,
                quality,
                title,
                duration,
                yt_url,
                yt_id,
                messy,
            )
        except FloodWait as e:
            await messy.edit(gm(chat_id, "error_flood").format(e.x))
            await sleep(e.x)
            await self._set_streaming(
                chat_id,
                user_id,
                video_url,
                quality,
                title,
                duration,
                yt_url,
                yt_id,
                messy,
            )
