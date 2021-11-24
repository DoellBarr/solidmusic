from typing import Dict

from pyrogram import idle
from pyrogram.types import CallbackQuery

from .telegram_call import TelegramPlayer
from .youtube_call import YoutubePlayer
from core import username as usernames

username = usernames


class MediaPlayer(TelegramPlayer, YoutubePlayer):
    async def join_call(
        self,
        stream_type: str,
        cb: CallbackQuery,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str
    ):
        if stream_type == "music":
            await self.play(cb, user_id, title, duration, yt_url, yt_id)
        elif stream_type == "video":
            await self.video_play(cb, user_id, title, duration, yt_url, yt_id)

    async def music_or_video(self, cb: CallbackQuery, result: Dict):
        user_id = int(result["user_id"])
        title = result["title"]
        duration = result["duration"]
        yt_url = result["yt_url"]
        yt_id = result["yt_id"]
        stream_type = result["stream_type"]
        await self.join_call(stream_type, cb, user_id, title, duration, yt_url, yt_id)

    async def run(self):
        print("[ INFO ] START BOT CLIENT")
        await self.bot.start()
        print("[ INFO ] GETTING BOT USERNAME")
        await self.get_username()
        print("[ INFO ] START PyTgCalls CLIENT")
        await self.call.start()
        print("[ INFO ] CLIENT RUNNING")
        await idle()
        print("[ INFO ] STOPPING BOT")
        await self.bot.stop()

    async def get_username(self):
        global username
        me = await self.bot.get_me()
        username += me.username


player = MediaPlayer()
