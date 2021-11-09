import random
from typing import List, Dict, Union

from pyrogram import types
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.types.input_stream import AudioPiped

from utils.functions.yt_utils import get_audio_direct_link
from .bot_base import bot_client
from .client_base import call_py, user


class CallBase:
    def __init__(self):
        self._bot = bot_client
        self._user = user
        self._call = call_py
        self._playlist: Dict[int, List[Dict[str, str]]] = {}

    def extend_playlist(
        self,
        user_id: int,
        chat_id: int,
        title: str,
        duration: Union[str, int],
        yt_url: str,
        yt_id: str,
        stream_type: str,
    ):
        playlist = self._playlist
        playlist[chat_id].extend(
            [
                {
                    "user_id": user_id,
                    "title": title,
                    "duration": duration,
                    "yt_url": yt_url,
                    "yt_id": yt_id,
                    "stream_type": stream_type,
                }
            ]
        )

    def is_call_active(self, chat_id: int):
        call = self._call
        for active_call in call.active_calls:
            if chat_id == active_call["chat_id"]:
                return True
            return False
        return None

    def send_playlist(self, chat_id: int):
        playlist = self._playlist
        current = playlist[chat_id][0]
        queued = playlist[chat_id][1:]
        return current, queued

    async def check_call(self, chat_id):
        call = self._call
        try:
            if call.get_call(chat_id):
                return True
        except GroupCallNotFound:
            await self.create_call(chat_id)
            return True

    async def end_stream(self, chat_id: int):
        call = self._call
        is_active = self.is_call_active(chat_id)
        if is_active:
            return await call.leave_group_call(chat_id)

    async def create_call(self, chat_id: int):
        return await self._user.send(
            CreateGroupCall(
                peer=await self._user.resolve_peer(chat_id),
                random_id=random.randint(10000, 999999999),
            )
        )

    async def leave_group_call(self, chat_id: int):
        call = self._call
        return await call.leave_group_call(chat_id)

    async def change_vol(self, chat_id: int, vol: int):
        call = self._call
        is_active = self.is_call_active(chat_id)
        if is_active:
            return await call.change_volume_call(chat_id, vol)
        return None

    async def change_streaming_status(self, status: str, chat_id: int):
        call = self._call
        is_active = self.is_call_active(chat_id)
        if is_active:
            if status == "pause":
                return await call.pause_stream(chat_id)
            if status == "resume":
                return await call.resume_stream(chat_id)
            return
        return None

    async def stream_change(self, chat_id: int, yt_url: str):
        call = self._call
        url = get_audio_direct_link(yt_url)
        await call.change_stream(chat_id, AudioPiped(url))

    async def change_stream(self, chat_id: int):
        playlist = self._playlist
        if len(playlist[chat_id]) > 1:
            old_playlist = playlist[chat_id].pop(0)
            old_title = old_playlist["title"]
            yt_url = playlist[chat_id][0]["yt_url"]
            title = playlist[chat_id][0]["title"]
            await self.stream_change(chat_id, yt_url)
            return "track_skipped"
        return "no_playlists"
