from typing import Dict

from pyrogram import types

from .music_base import MusicPlayer
from .video_base import VideoPlayer


class Methods(
    MusicPlayer,
    VideoPlayer
):
    pass


class Player(Methods):
    def __init__(self):
        super().__init__()

    async def play_or_stream(self, cb: types.CallbackQuery, result: Dict):
        playlist = self._playlist
        chat_id = cb.message.chat.id

        user_id = result["user_id"]
        title = result["title"]
        duration = result["duration"]
        yt_url = result["yt_url"]
        yt_id = result["yt_id"]
        stream_type = result["stream_type"]

        if stream_type == "music":
            return await self._play(
                cb,
                user_id,
                title,
                duration,
                yt_url,
                yt_id
            )
        if stream_type == "video":
            quality = result["quality"]
            return await self._stream(
                cb,
                user_id,
                title,
                duration,
                yt_url,
                yt_id,
                quality
            )


player = Player()
