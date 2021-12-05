import os.path
import shutil
import sys
from typing import Dict

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.errors import UserAlreadyParticipant

from configs import config
from pyrogram import idle
from pyrogram.types import CallbackQuery

from .calls import leave_from_inactive_call
from .telegram_call import TelegramPlayer
from .youtube_call import YoutubePlayer
from core import username as usernames
from plugins import load_module

username = usernames
scheduler = AsyncIOScheduler()


class MediaPlayer(TelegramPlayer, YoutubePlayer):
    async def join_call(
        self,
        stream_type: str,
        cb: CallbackQuery,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
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
        self.db.init()
        print("⌈ [ INFO ] START BOT CLIENT")
        await self.bot.start()
        print("|- [ INFO ] LOAD ALL MODULES")
        load_module()
        print("|- [ INFO ] GETTING BOT USERNAME")
        await self.get_username()
        print("⌊ [ INFO ] START PyTgCalls CLIENT")
        await self.call.start()
        await self.join_channel()
        if config.AUTO_LEAVE:
            print("[ INFO ] STARTING SCHEDULER")
            scheduler.configure(timezone=pytz.utc)
            scheduler.add_job(
                leave_from_inactive_call, "interval", seconds=config.AUTO_LEAVE
            )
            scheduler.start()
        else:
            pass
        print("[ INFO ] CLIENT RUNNING")
        await idle()
        print("[ INFO ] STOPPING BOT")
        self.db.close()
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
        if os.path.exists("search"):
            shutil.rmtree("search")
        await self.bot.stop()
        sys.exit()

    async def get_username(self):
        global username
        me = await self.bot.get_me()
        username += me.username

    async def join_channel(self):
        try:
            await self.user.join_chat("solidprojects")
        except UserAlreadyParticipant:
            pass


player = MediaPlayer()
