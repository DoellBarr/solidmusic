from typing import Dict

from pyrogram import types
from pytgcalls import idle

from .music_base import MusicPlayer
from .video_base import VideoPlayer


class Methods(MusicPlayer, VideoPlayer):
    pass


class Player(Methods):
    async def play_or_stream(self, cb: types.CallbackQuery, result: Dict):
        user_id = result["user_id"]
        title = result["title"]
        duration = result["duration"]
        yt_url = result["yt_url"]
        yt_id = result["yt_id"]
        stream_type = result["stream_type"]

        if stream_type == "music":
            return await self._play(cb, user_id, title, duration, yt_url, yt_id)
        if stream_type == "video":
            quality = result["quality"]
            return await self._stream(
                cb, user_id, title, duration, yt_url, yt_id, quality
            )

    async def start(self):
        print("[ INFO ] STARTING BOT CLIENT")
        await self._bot.start()
        print("[ INFO ] STARTING PyTgCalls CLIENT")
        await self._call.start()
        print("[ INFO ] CLIENT RUNNING")
        await idle()
        print("[ INFO ] STOPPING BOT")
        await self._bot.stop()


player = Player()
