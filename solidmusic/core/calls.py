from random import randint

from pyrogram.errors import (
    ChatAdminRequired,
    ChannelPrivate,
    ChatForbidden,
    PeerIdInvalid,
    UserAlreadyParticipant,
)

from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.types import Message
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    LowQualityAudio,
    LowQualityVideo,
    MediumQualityAudio,
    MediumQualityVideo,
    HighQualityVideo,
    HighQualityAudio,
)

from solidmusic.core.client import user, bot, call_py
from solidmusic.core.song_queue import queue
from solidmusic.database.chat_db import ChatDB
from solidmusic.database.lang_utils import gm
from solidmusic.database.sudo_db import SudoDB
from solidmusic.functions.yt_utils import get_audio_direct_link, get_video_direct_link


class Methods(ChatDB, SudoDB):
    pass


class Call:
    def __init__(self):
        self.db = Methods()
        self.call = call_py
        self.user = user
        self.bot = bot
        self.playlist = queue

    async def get_quality(self, chat_id: int):
        quality: str = (await self.db.get_chat(chat_id)).get("quality")
        if quality not in {"low", "medium", "high"}:
            raise KeyError("Invalid Quality, Valid Quality is low, medium, high")
        audio_quality = (
            LowQualityAudio()
            if quality == "low"
            else MediumQualityAudio()
            if quality == "medium"
            else HighQualityAudio()
        )
        video_quality = (
            LowQualityVideo()
            if quality == "low"
            else MediumQualityVideo()
            if quality == "medium"
            else HighQualityVideo()
        )
        return audio_quality, video_quality

    async def init_youtube_player(
        self,
        chat_id: int,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
        stream_type: str,
    ):
        datas = {
            "user_id": user_id,
            "title": title,
            "duration": duration,
            "yt_url": yt_url,
            "yt_id": yt_id,
            "stream_type": stream_type,
        }
        return await self.playlist.insert_one(chat_id, datas)

    async def init_telegram_player(
        self,
        chat_id: int,
        user_id: int,
        title: str,
        duration: str,
        source_file: str,
        link: str,
        stream_type: str,
    ):
        datas = {
            "user_id": user_id,
            "title": title,
            "duration": duration,
            "source_file": source_file,
            "link": link,
            "stream_type": stream_type,
        }
        return await self.playlist.insert_one(chat_id, datas)

    async def get_call(self, chat_id: int):
        call = self.call
        try:
            if call.get_call(chat_id):
                return await call.get_call(chat_id)
        except GroupCallNotFound:
            return False

    async def start_call(self, m: Message):
        chat_id = m.chat.id
        bot_id = (await self.bot.get_me()).id
        user_id = (await self.user.get_me()).id
        try:
            if self.get_call(chat_id):
                pass
            await self.user.send(
                CreateGroupCall(
                    peer=await self.user.resolve_peer(chat_id),
                    random_id=randint(int(1e4), int("9" * 9)),
                )
            )
            return await m.reply(await gm(chat_id, "call_started"))
        except (ChannelPrivate, ChatForbidden):
            try:
                await m.chat.unban_member(user_id)
                return await self.start_call(m)
            except PeerIdInvalid:
                await self.user.send_message(bot_id, "/start")
                return await self.start_call(m)
            except (ChatForbidden, ChannelPrivate):
                await self.playlist.delete_chat(chat_id)
                return await m.reply(await gm(chat_id, "user_banned"))
        except ChatAdminRequired:
            try:
                await m.chat.promote_member(user_id)
                return await self.start_call(m)
            except PeerIdInvalid:
                await self.user.send_message(bot_id, "/start")
                await m.chat.promote_member(user_id)
                return await self.start_call(m)

    async def end_call(self, m: Message):
        chat_id = m.chat.id
        if call := await self.get_call(chat_id):
            await self.user.send(DiscardGroupCall(call=call))
            return await m.reply(await gm(chat_id, "call_closed"))

    async def change_vol(self, m: Message):
        volume = int(m.command[1])
        call = self.call
        chat_id = m.chat.id
        if await self.get_call(chat_id):
            await call.change_volume_call(chat_id, volume)
            return await m.reply(await gm(chat_id, "volume_changed", [f"{volume}"]), )
        return await m.reply(await gm(chat_id, "not_in_call"))

    async def change_streaming_status(self, status: str, m: Message):
        call = self.call
        chat_id = m.chat.id
        if not await self.get_call(chat_id):
            return await m.reply(await gm(chat_id, "not_in_call"))
        if status == "pause":
            await call.pause_stream(chat_id)
            return await m.reply(await gm(chat_id, "track_paused"))
        if status == "resume":
            await call.resume_stream(chat_id)
            return await m.reply(await gm(chat_id, "track_resumed"))

    async def end_stream(self, m: Message):
        chat_id = m.chat.id
        call = self.call
        if await self.get_call(chat_id):
            await call.leave_group_call(chat_id)
            await self.playlist.delete_chat(chat_id)
            return await m.reply(await gm(chat_id, "stream_ended"))
        return await m.reply(await gm(chat_id, "not_in_call"))

    async def _change_stream(self, chat_id: int):
        playlist = self.playlist
        await playlist.delete_one(chat_id)
        title = (await playlist.get_queue(chat_id)).get("title")
        stream_type = (await playlist.get_queue(chat_id)).get("stream_type")
        if stream_type in {"video", "music"}:
            yt_url = (await playlist.get_queue(chat_id)).get("yt_url")
            return await self._stream_change(chat_id, yt_url, stream_type)
        if stream_type in {"local_video", "local_music"}:
            return await self._stream_change(chat_id, stream_type=stream_type)
        return title

    async def _stream_change(
        self, chat_id: int, yt_url: str = None, stream_type: str = None
    ):
        call = self.call
        if stream_type == "music":
            url = await get_audio_direct_link(yt_url)
            audio_quality, _ = await self.get_quality(chat_id)
            stream = AudioPiped(url, audio_quality)
        elif stream_type == "video":
            path = await get_video_direct_link(yt_url)
            audio_parameters, video_parameters = await self.get_quality(chat_id)
            stream = AudioVideoPiped(path, audio_parameters, video_parameters)
        elif stream_type == "local_music":
            audio_parameters, _ = await self.get_quality(chat_id)
            path = (await self.playlist.get_queue(chat_id)).get("source_file")
            stream = AudioPiped(path, audio_parameters)
        else:
            audio_parameters, video_parameters = await self.get_quality(chat_id)
            path = (await self.playlist.get_queue(chat_id)).get("source_file")
            stream = AudioVideoPiped(path, audio_parameters, video_parameters)
        await call.change_stream(chat_id, stream)

    async def change_stream(self, m: Message):
        chat_id = m.chat.id
        playlist = self.playlist.playlist
        if chat_id in playlist and len(playlist[chat_id]) > 1:
            title = await self._change_stream(chat_id)
            return await m.reply(await gm(chat_id, "track_skipped", [title]))
        return await m.reply(await gm(chat_id, "no_playlists"))

    async def join_chat(self, m: Message):
        link = await m.chat.export_invite_link()
        chat_id = m.chat.id
        try:
            await self.user.join_chat(link)
            user_id = (await self.user.get_me()).id
            await m.chat.promote_member(user_id)
        except ChatAdminRequired:
            await self.playlist.delete_chat(chat_id)
            return await m.reply(await gm(chat_id, "need_add_user_permission"))
        except UserAlreadyParticipant:
            pass

    async def send_playlist(self, chat_id: int):
        playlist = self.playlist.playlist
        if chat_id in playlist:
            current = playlist[chat_id][0]
            queued = playlist[chat_id][1:]
            return current, queued
        return None, None
