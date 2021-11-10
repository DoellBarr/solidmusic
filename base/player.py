from typing import Dict

from pyrogram import types
from pytgcalls import idle

from .music_base import MusicPlayer
from .video_base import VideoPlayer
from .bot_base import pyro_bot
from .client_base import call_py


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
            return await self.play(cb, user_id, title, duration, yt_url, yt_id)
        if stream_type == "stream":
            quality = result["quality"]
            return await self.stream(
                cb, user_id, title, duration, yt_url, yt_id, quality
            )

    @staticmethod
    async def start():
        print("[ INFO ] STARTING BOT CLIENT")
        await pyro_bot.start()
        print("[ INFO ] STARTING PyTgCalls CLIENT")
        await call_py.start()
        print("[ INFO ] CLIENT RUNNING")
        await idle()
        print("[ INFO ] STOPPING BOT")
        await pyro_bot.stop()


player = Player()
