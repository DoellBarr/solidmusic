import random
from typing import List, Dict, Union

from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped

from utils.functions.yt_utils import get_audio_direct_link
from .bot_base import bot_client
from .client_base import call_py, user

from dB.lang_utils import get_message as gm


class CallBase:
    def __init__(self):
        self.bot = bot_client
        self.user = user
        self.call = call_py
        self.playlist: Dict[int, List[Dict[str, str]]] = {}

        @self.call.on_stream_end()
        async def _(_, update: Update):
            playlist = self.playlist
            call = self.call
            chat_id = update.chat_id
            if len(playlist[chat_id]) > 1:
                playlist[chat_id].pop(0)
                yt_url = playlist[chat_id][0]["yt_url"]
                return await self.stream_change(chat_id, yt_url)
            await call.leave_group_call(chat_id)
            del playlist[chat_id]

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
        playlist = self.playlist
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
        call = self.call
        for active_call in call.calls:
            if chat_id == getattr(active_call, "chat_id"):
                return True
            else:
                return False
        return False

    def send_playlist(self, chat_id: int):
        playlist = self.playlist
        current = playlist[chat_id][0]
        queued = playlist[chat_id][1:]
        return current, queued

    async def check_call(self, chat_id):
        call = self.call
        try:
            if call.get_call(chat_id):
                return True
        except GroupCallNotFound:
            await self.create_call(chat_id)
            return True

    async def end_stream(self, chat_id: int):
        call = self.call
        is_active = self.is_call_active(chat_id)
        if is_active:
            return await call.leave_group_call(chat_id)

    async def create_call(self, chat_id: int):
        return await self.user.send(
            CreateGroupCall(
                peer=await self.user.resolve_peer(chat_id),
                random_id=random.randint(10000, 999999999),
            )
        )

    async def leave_group_call(self, chat_id: int):
        call = self.call
        return await call.leave_group_call(chat_id)

    async def change_vol(self, chat_id: int, vol: int):
        call = self.call
        is_active = self.is_call_active(chat_id)
        if is_active:
            return await call.change_volume_call(chat_id, vol)
        return None

    async def change_streaming_status(self, status: str, chat_id: int):
        call = self.call
        is_active = self.is_call_active(chat_id)
        if is_active:
            if status == "pause":
                await call.pause_stream(chat_id)
                return "track_paused"
            if status == "resume":
                await call.resume_stream(chat_id)
                return "track_resumed"
        else:
            return "not_streaming"

    async def stream_change(self, chat_id: int, yt_url: str):
        call = self.call
        url = get_audio_direct_link(yt_url)
        await call.change_stream(chat_id, AudioPiped(url))

    async def change_stream(self, chat_id: int):
        playlist = self.playlist
        if len(playlist[chat_id]) > 1:
            yt_url = playlist[chat_id][0]["yt_url"]
            title = playlist[chat_id][0]["title"]
            await self.stream_change(chat_id, yt_url)
            toks = gm(chat_id, "track_skipped").format(title)
            return toks
        return "no_playlists"
