import asyncio
import datetime

from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped

from .calls import Call
from database.lang_utils import get_message as gm


class TelegramPlayer(Call):
    async def _local_audio_play(
        self,
        mess: Message,
        user_id: int,
        chat_id: int,
        title: str,
        duration: str,
        source_file: str,
        link: str,
    ):
        mention = await self.bot.get_user_mention(user_id)
        call = self.call
        self.init_telegram_player(
            chat_id, user_id, title, duration, source_file, link, "local_music"
        )
        audio_quality, _ = self.get_quality(chat_id)
        try:
            await call.join_group_call(
                chat_id,
                AudioPiped(source_file, audio_quality),
                stream_type=StreamType().local_stream,
            )
            return await mess.edit(
                f"""
{gm(chat_id, 'now_streaming')}
📌 {gm(chat_id, 'yt_title')}: [{title}]({link}) 
⏱️ {gm(chat_id, 'duration')}: {duration}
✨ {gm(chat_id, 'req_by')}: {mention}
🎥 {gm(chat_id, 'stream_type_title')}: {gm(chat_id, 'stream_type_local_audio')}""",
                disable_web_page_preview=True,
            )
        except NoActiveGroupCall:
            await self.start_call(chat_id)
            await self._local_audio_play(
                mess, user_id, chat_id, title, duration, source_file, link
            )
        except FloodWait as e:
            await mess.edit(gm(chat_id, "error_flood".format(str(e.x))))
            await asyncio.sleep(e.x)
            await self._local_audio_play(
                mess, user_id, chat_id, title, duration, source_file, link
            )
        except UserNotParticipant:
            await self.join_chat(chat_id)
            await self._local_audio_play(
                mess, user_id, chat_id, title, duration, source_file, link
            )

    async def _local_video_play(
        self,
        mess: Message,
        user_id: int,
        chat_id: int,
        title: str,
        duration: str,
        source_file: str,
        link: str,
    ):
        call = self.call
        mention = await self.bot.get_user_mention(user_id)
        self.init_telegram_player(
            chat_id, user_id, title, duration, source_file, link, "video_file"
        )
        audio_quality, video_quality = self.get_quality(chat_id)
        try:
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(source_file, audio_quality, video_quality),
                stream_type=StreamType().local_stream,
            )
            return await mess.edit(
                f"""
{gm(chat_id, 'now_streaming')}
📌 {gm(chat_id, 'yt_title')}: [{title}]({link}) 
⏱️ {gm(chat_id, 'duration')}: {duration}
✨ {gm(chat_id, 'req_by')}: {mention}
🎥 {gm(chat_id, 'stream_type_title')}: {gm(chat_id, 'stream_type_local_video')}""",
                disable_web_page_preview=True,
            )
        except NoActiveGroupCall:
            await self.start_call(chat_id)
            await self._local_video_play(
                mess, user_id, chat_id, title, duration, source_file, link
            )
        except FloodWait as e:
            await mess.edit(gm(chat_id, "error_flood".format(str(e.x))))
            await self._local_video_play(
                mess, user_id, chat_id, title, duration, source_file, link
            )
        except UserNotParticipant:
            await self.join_chat(chat_id)
            await self._local_video_play(
                mess, user_id, chat_id, title, duration, source_file, link
            )

    async def local_music(self, user_id: int, replied: Message):
        chat_id = replied.chat.id
        playlist = self.playlist.playlist
        if replied.audio or replied.voice:
            bom = await replied.reply(gm(chat_id, "process"))
            download = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    title = replied.audio.title[:36]
                    duration = replied.audio.duration
                elif replied.audio.file_name:
                    title = replied.audio.file_name[:36]
                    duration = replied.audio.duration
                else:
                    title = "Music"
                    duration = replied.audio.duration
            else:
                title = "Voice Note"
                duration = replied.voice.duration
            duration = str(datetime.timedelta(seconds=duration))
            if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
                objects = {
                    "user_id": user_id,
                    "title": title,
                    "duration": duration,
                    "source_file": download,
                    "link": link,
                    "stream_type": "local_music",
                }
                mess = await bom.edit(gm(chat_id, "track_queued"))
                self.playlist.insert_one(chat_id, objects)
                await asyncio.sleep(5)
                return await mess.delete()
            return await self._local_audio_play(
                bom, user_id, chat_id, title, duration, download, link
            )

    async def local_video(self, user_id: int, replied: Message):
        chat_id = replied.chat.id
        playlist = self.playlist.playlist
        if replied.video or replied.document:
            bom = await replied.reply(gm(chat_id, "process"))
            source_file = await replied.download()
            link = replied.link
            if replied.video:
                title = replied.video.file_name[:36]
                duration = replied.video.duration
            else:
                title = replied.document.file_name[:36]
                duration = "Not Found"
            if duration:
                duration = str(datetime.timedelta(seconds=duration))
            else:
                duration = "Not Found"
            if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
                objects = {
                    "user_id": user_id,
                    "title": title,
                    "duration": duration,
                    "source_file": source_file,
                    "link": link,
                    "stream_type": "local_video",
                }
                mess = await bom.edit(gm(chat_id, "track_queued"))
                self.playlist.insert_one(chat_id, objects)
                await asyncio.sleep(5)
                return mess.delete()
            return await self._local_video_play(
                bom, user_id, chat_id, title, duration, source_file, link
            )
