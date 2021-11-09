from typing import Dict

from pyrogram import types
from pytgcalls import idle
from pytgcalls.types import Update

from .music_base import MusicPlayer
from .video_base import VideoPlayer


class Methods(MusicPlayer, VideoPlayer):
    pass


class Player(Methods):
    def __init__(self):

        super().__init__()
        self._play = super()._play
        self._stream = super()._stream
        self._bot = super()._bot

        call = super()._call
        playlist = super()._playlist

        @call.on_stream_end()
        async def on_stream_end_(_, update: Update):
            chat_id = update.chat_id
            if len(playlist[chat_id]) > 1:
                playlist[chat_id].pop(0)
                yt_url = playlist[chat_id][0]["yt_url"]
                return await self.stream_change(chat_id, yt_url)
            await call.leave_group_call(chat_id)
            del playlist[chat_id]

    async def play_or_stream(self, cb: types.CallbackQuery, result: Dict):
        user_id = result["user_id"]
        title = result["title"]
        duration = result["duration"]
        yt_url = result["yt_url"]
        yt_id = result["yt_id"]
        stream_type = result["stream_type"]

        if stream_type == "music":
            return await self._play(cb, user_id, title, duration, yt_url, yt_id)
        if stream_type == "stream":
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
