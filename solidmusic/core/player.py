import sys

from pyrogram.types import CallbackQuery

import solidmusic.core

from .telegram_calls import TelegramPlayer
from .youtube_calls import YoutubePlayer

from pyrogram import idle
from pyrogram.errors import UserAlreadyParticipant

from os import path
from shutil import rmtree

from solidmusic.plugins import load_module


class Player(TelegramPlayer, YoutubePlayer):
    async def join_call(
        self,
        cb: CallbackQuery,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
        stream_type: str,
    ):
        return await self.stream(cb, title, duration, yt_url, yt_id, stream_type)

    async def start_stream(self, cb: CallbackQuery, results: dict[str, str]):
        title, duration, yt_url, yt_id, stream_type = results.values()
        return await self.join_call(cb, title, duration, yt_url, yt_id, stream_type)

    async def run(self):
        await self.db.init()
        print("[+] START BOT CLIENT")
        await self.bot.start()
        await self.user.start()
        print("[+] LOAD ALL MODULES")
        load_module()
        print("[+] Getting Bot Username".upper())
        bot_username = await self.bot.get_username()
        print(f"[+] Bot Username: {bot_username}")
        solidmusic.core.username = bot_username
        print("[+] START PyTgCalls CLIENT")
        await self.call.start()
        try:
            await self.user.join_chat("SolidProjectsReborn")
        except UserAlreadyParticipant:
            pass
        print("[+] CLIENT RUNNING")
        await idle()
        print("[+] STOPPING BOT")
        await self.db.disconnect()
        if path.exists("downloads"):
            rmtree("downloads")
        if path.exists("image"):
            rmtree("image")
        await self.bot.stop()
        return sys.exit()


player = Player()
