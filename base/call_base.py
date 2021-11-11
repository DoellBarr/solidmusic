import random
from typing import List, Dict, Union

from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, LowQualityVideo, MediumQualityVideo, HighQualityVideo

from dB.database import db
from utils.functions.yt_utils import get_audio_direct_link, get_video_direct_link
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
                title = playlist[chat_id][0]["title"]
                stream_type = playlist[chat_id][0]["stream_type"]
                await self.stream_change(chat_id, yt_url, stream_type)
                await self.bot.send_to_chat(
                    chat_id,
                    "track_changed",
                    title
                )
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
        return False

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
        return False

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

    async def stream_change(self, chat_id: int, yt_url: str, stream_type: str):
        call = self.call
        if stream_type == "music":
            url = get_audio_direct_link(yt_url)
            await call.change_stream(chat_id, AudioPiped(url))
        elif stream_type == "stream":
            quality = db.get_chat(chat_id)[0]["video_quality"]
            url = get_video_direct_link(yt_url, quality)
            if quality == "low":
                video_quality = LowQualityVideo()
            elif quality == "medium":
                video_quality = MediumQualityVideo()
            else:
                video_quality = HighQualityVideo()
            await call.change_stream(
                chat_id,
                AudioVideoPiped(url, HighQualityAudio(), video_quality)
            )

    async def change_stream(self, chat_id: int):
        playlist = self.playlist
        if len(playlist[chat_id]) > 1:
            yt_url = playlist[chat_id][0]["yt_url"]
            title = playlist[chat_id][0]["title"]
            stream_type = playlist[chat_id][0]["stream_type"]
            await self.stream_change(chat_id, yt_url, stream_type)
            toks = "track_skipped"
            return toks, title
        return "no_playlists", ""
