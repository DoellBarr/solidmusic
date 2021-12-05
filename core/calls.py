import asyncio
import random

from pyrogram.errors import (
    UserNotParticipant,
    ChatAdminRequired,
    ChannelPrivate,
    ChatForbidden,
    PeerIdInvalid,
    UserAlreadyParticipant,
)
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    LowQualityAudio,
    MediumQualityAudio,
    HighQualityAudio,
    LowQualityVideo,
    MediumQualityVideo,
    HighQualityVideo,
)
from pytgcalls.types.stream import StreamAudioEnded

from functions.youtube_utils import get_audio_direct_link, get_video_direct_link
from .clients import user, call_py
from .bot import Bot
from .queue import Queue
from database.chat_database import ChatDB
from database.sudo_database import SudoDB


class Methods(ChatDB, SudoDB):
    pass


async def leave_from_inactive_call():
    all_chat_id = []
    async for chat in user.iter_dialogs():
        chat_id = chat.chat.id
        if chat.chat.type in ["group", "supergroup"]:
            for call in call_py.calls:
                call_chat_id = int(getattr(call, "chat_id"))
                if call_chat_id in all_chat_id:
                    pass
                else:
                    all_chat_id.append(call_chat_id)
                call_status = getattr(call, "status")
                try:
                    if call_chat_id == chat_id and call_status == "not_playing":
                        await user.leave_chat(chat_id)
                    elif chat_id not in all_chat_id:
                        await user.leave_chat(chat_id)
                except UserNotParticipant:
                    pass
            if chat_id not in all_chat_id:
                try:
                    await user.leave_chat(chat_id)
                except PeerIdInvalid:
                    pass


class Call:
    def __init__(self):
        self.call = call_py
        self.user = user
        self.bot = Bot()
        self.playlist = Queue()
        self.db = Methods()

        @self.call.on_stream_end()
        async def _(_, update: Update):
            if isinstance(update, StreamAudioEnded):
                chat_id = update.chat_id
                await self.check_playlist(chat_id)

        @self.call.on_kicked()
        @self.call.on_left()
        @self.call.on_closed_voice_chat()
        async def __(_, chat_id: int):
            return self.playlist.delete_chat(chat_id)

    def get_quality(self, chat_id):
        quality: str = self.db.get_chat(chat_id)[0]["quality"]
        if quality not in ["low", "medium", "high"]:
            raise KeyError("Invalid Quality")
        if quality == "low":
            audio_quality = LowQualityAudio()
            video_quality = LowQualityVideo()
        elif quality == "medium":
            audio_quality = MediumQualityAudio()
            video_quality = MediumQualityVideo()
        else:
            audio_quality = HighQualityAudio()
            video_quality = HighQualityVideo()
        return audio_quality, video_quality

    def init_youtube_player(
        self,
        chat_id: int,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
        stream_type: str,
    ):
        objects = {
            "user_id": user_id,
            "title": title,
            "duration": duration,
            "yt_url": yt_url,
            "yt_id": yt_id,
            "stream_type": stream_type,
        }
        return self.playlist.insert_one(chat_id, objects)

    def init_telegram_player(
        self,
        chat_id: int,
        user_id: int,
        title: str,
        duration: str,
        source_file: str,
        link: str,
        stream_type: str,
    ):
        objects = {
            "user_id": user_id,
            "title": title,
            "duration": duration,
            "source_file": source_file,
            "link": link,
            "stream_type": stream_type,
        }
        return self.playlist.insert_one(chat_id, objects)

    def is_call_active(self, chat_id: int):
        call = self.call
        try:
            if call.get_call(chat_id):
                return True
        except GroupCallNotFound:
            return False

    async def start_call(self, chat_id: int):
        users = self.user
        try:
            is_active = self.is_call_active(chat_id)
            if not is_active:
                await users.send(
                    CreateGroupCall(
                        peer=await users.resolve_peer(chat_id),
                        random_id=random.randint(10000, 999999999),
                    )
                )
                await self.bot.send_message(chat_id, "call_started")
            else:
                pass
        except (ChannelPrivate, ChatForbidden):
            try:
                await self.bot.unban_member(chat_id, (await self.bot.get_me()).id)
                await self.start_call(chat_id)
            except PeerIdInvalid:
                await users.send_message((await self.bot.get_me()).id, "/start")
                await self.start_call(chat_id)
            except (ChatForbidden, ChannelPrivate):
                self.playlist.delete_chat(chat_id)
                return await self.bot.send_message(chat_id, "user_banned")
        except ChatAdminRequired:
            try:
                await self.bot.promote_member(chat_id, (await users.get_me()).id)
                await self.start_call(chat_id)
            except PeerIdInvalid:
                await users.send_message((await self.bot.get_me()).id, "/start")
                await self.bot.promote_member(chat_id, (await users.get_me()).id)
                await self.start_call(chat_id)

    async def end_call(self, chat_id: int):
        # Credit Userge
        try:
            call = await self.call.get_call(chat_id)
            await self.user.send(DiscardGroupCall(call=call))
            await self.bot.send_message(chat_id, "call_closed")
        except GroupCallNotFound:
            await self.bot.send_message(chat_id, "no_active_group_call")

    async def change_vol(self, chat_id: int, volume: int):
        call = self.call
        is_active = self.is_call_active(chat_id)
        if is_active:
            await call.change_volume_call(chat_id, volume)
            return await self.bot.send_message(chat_id, "volume_changed", str(volume))
        return await self.bot.send_message(chat_id, "not_in_call")

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
            return "not_in_call"

    async def end_stream(self, chat_id: int):
        call = self.call
        is_active = self.is_call_active(chat_id)
        if is_active:
            await call.leave_group_call(chat_id)
            self.playlist.delete_chat(chat_id)
            return "stream_ended"
        return "not_in_call"

    async def _change_stream(self, chat_id: int):
        playlist = self.playlist
        playlist.delete_one(chat_id)
        title = playlist.get(chat_id)["title"]
        stream_type = playlist.get(chat_id)["stream_type"]
        if stream_type in ["video", "music"]:
            yt_url = playlist.get(chat_id)["yt_url"]
            await self._stream_change(chat_id, yt_url, stream_type)
        elif stream_type in ["local_video", "local_music"]:
            await self._stream_change(chat_id, stream_type=stream_type)
        return title

    async def _stream_change(self, chat_id: int, yt_url: str = None, stream_type: str = None):
        call = self.call
        if stream_type == "music":
            url = get_audio_direct_link(yt_url)
            quality, _ = self.get_quality(chat_id)
            await call.change_stream(chat_id, AudioPiped(url, quality))
        elif stream_type == "video":
            url = get_video_direct_link(yt_url)
            audio_quality, video_quality = self.get_quality(chat_id)
            await call.change_stream(
                chat_id, AudioVideoPiped(url, audio_quality, video_quality)
            )
        elif stream_type == "local_music":
            audio_quality, _ = self.get_quality(chat_id)
            local_audio = self.playlist.get(chat_id)["source_file"]
            await call.change_stream(
                chat_id, AudioPiped(local_audio, audio_quality)
            )
        elif stream_type == "local_video":
            audio_quality, video_quality = self.get_quality(chat_id)
            source_file = self.playlist.get(chat_id)["source_file"]
            await call.change_stream(
                chat_id, AudioVideoPiped(source_file, audio_quality, video_quality)
            )

    async def check_playlist(self, chat_id: int):
        playlist = self.playlist.playlist
        call = self.call
        if playlist and chat_id in playlist:
            if len(playlist[chat_id]) > 1:
                title = await self._change_stream(chat_id)
                await self.bot.send_message(chat_id, "track_changed", title, delete=5)
            elif len(playlist[chat_id]) == 1:
                await call.leave_group_call(chat_id)
                self.playlist.delete_chat(chat_id)
        else:
            await call.leave_group_call(chat_id)

    async def change_stream(self, chat_id: int):
        playlist = self.playlist.playlist
        if chat_id in playlist and len(playlist[chat_id]) > 1:
            title = await self._change_stream(chat_id)
            return await self.bot.send_message(
                chat_id, "track_skipped", title, delete=5
            )
        return await self.bot.send_message(chat_id, "no_playlists")

    async def join_chat(self, chat_id: int):
        link = await self.bot.export_chat_invite_link(chat_id)
        if "+" in link:
            link_hash = (link.replace("+", "")).split("t.me/")[1]
            try:
                await self.user.join_chat(f"https://t.me/joinchat/{link_hash}")
                client_user_id = (await self.user.get_me()).id
                await self.bot.promote_member(chat_id, client_user_id)
            except ChatAdminRequired:
                self.playlist.delete_chat(chat_id)
                return await self.bot.send_message(chat_id, "need_add_user_permission")
            except UserAlreadyParticipant:
                pass
            await asyncio.sleep(3)
            await self.bot.revoke_chat_invite_link(chat_id, link)

    def send_playlist(self, chat_id: int):
        playlist = self.playlist.playlist
        if chat_id in playlist:
            current = playlist[chat_id][0]
            queued = playlist[chat_id][1:]
            return current, queued
        return None, None
