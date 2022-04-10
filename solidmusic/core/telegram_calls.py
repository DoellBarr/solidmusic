import asyncio
from datetime import timedelta as td

from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped


from solidmusic.core.calls import Call
from solidmusic.database.lang_utils import gm


class TelegramPlayer(Call):
    async def _local_audio_play(
        self, m: Message, title: str, duration: str, source_file: str, link: str
    ):
        call = self.call
        chat_id = m.chat.id
        user_id = m.from_user.id
        mention = m.from_user.mention
        await self.init_telegram_player(
            chat_id, user_id, title, duration, source_file, link, "local_music"
        )
        audio_parameters, _ = await self.get_quality(chat_id)
        try:
            await call.join_group_call(
                chat_id,
                AudioPiped(source_file, audio_parameters),
                stream_type=StreamType().pulse_stream,
            )
            return await m.edit(
                f"""
{await gm(chat_id, 'now_streaming')}
{await gm(chat_id, 'yt_title')}: [{title}]({link})
{await gm(chat_id, 'duration')}: {duration}
{await gm(chat_id, 'req_by')}: {mention}
{await gm(chat_id, 'stream_type_title')}: {await gm(chat_id, 'stream_type_local_audio')}
                """,
                disable_web_page_preview=True,
            )
        except NoActiveGroupCall:
            await self.start_call(m)
            return await self._local_audio_play(m, title, duration, source_file, link)
        except FloodWait as e:
            await m.edit(await gm(chat_id, "error_flood", [f"{e.x}"]))
            await asyncio.sleep(e.x)
            return await self._local_audio_play(m, title, duration, source_file, link)
        except UserNotParticipant:
            await self.join_chat(m)
            return await self._local_audio_play(m, title, duration, source_file, link)

    async def _local_video_play(
        self, m: Message, title: str, duration: str, source_file: str, link: str
    ):
        call = self.call
        mention = m.from_user.mention
        user_id = m.from_user.id
        chat_id = m.chat.id
        await self.init_telegram_player(
            chat_id, user_id, title, duration, source_file, link, "local_video"
        )
        audio_parameters, video_parameters = await self.get_quality(chat_id)
        try:
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(source_file, audio_parameters, video_parameters),
                stream_type=StreamType().pulse_stream,
            )
            return await m.edit(
                f"""
{await gm(chat_id, 'now_streaming')}
{await gm(chat_id, 'yt_title')}: [{title}]({link})
{await gm(chat_id, 'duration')}: {duration}
{await gm(chat_id, 'req_by')}: {mention}
{await gm(chat_id, 'stream_type_title')}: {await gm(chat_id, 'stream_type_local_video')}
                """,
                disable_web_page_preview=True,
            )
        except NoActiveGroupCall:
            await self.start_call(m)
            return await self._local_video_play(m, title, duration, source_file, link)
        except FloodWait as e:
            await m.edit(await gm(chat_id, "error_flood", [f"{e.x}"]))
            await asyncio.sleep(e.x)
            return await self._local_video_play(m, title, duration, source_file, link)
        except UserNotParticipant:
            await self.join_chat(m)
            return await self._local_video_play(m, title, duration, source_file, link)

    async def play_music(self, m: Message):
        if not m.audio or m.voice:
            return await m.reply("reply_to_audio_message")
        chat_id = m.chat.id
        user_id = m.from_user.id
        playlist = self.playlist.playlist
        msg = await m.reply("process")
        link = m.link
        duration_limit = int((await self.db.get_chat(chat_id)).get("duration_limit"))
        duration = m.audio.duration if m.audio else m.voice.duration
        title = (
            (
                m.audio.title[:36]
                if m.audio.title
                else m.audio.file_name[:36]
                if m.audio.file_name
                else "Music"
            )
            if m.audio
            else "Voice Note"
        )
        if duration > duration_limit:
            return await msg.edit(
                await gm(chat_id, "duration_limit_exceeded", [f"{duration_limit}"])
            )
        download = await m.download()
        duration = str(td(seconds=duration))
        if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
            datas = {
                "user_id": user_id,
                "title": title,
                "duration": duration,
                "source_file": download,
                "link": link,
                "stream_type": "local_audio",
            }
            await self.playlist.insert_one(chat_id, datas)
            msg = await msg.edit(await gm(chat_id, "added_to_playlist", [title]))
            await asyncio.sleep(5)
            return await msg.delete()
        return await self._local_audio_play(msg, title, duration, download, link)

    async def play_video(self, m: Message):
        if not m.video or not m.document:
            return await m.reply("reply_to_video_message")
        chat_id = m.chat.id
        user_id = m.from_user.id
        playlist = self.playlist.playlist
        msg = await m.reply("process")
        link = m.link
        duration_limit = int((await self.db.get_chat(chat_id)).get("duration_limit"))
        duration = m.video.duration if m.video else "Not Available"
        source_file = await m.download()
        title = (
            (
                m.video.file_name[:36]
                if m.video.file_name
                else m.document.file_name[:36]
                if m.document.file_name
                else "Video"
            )
            if m.video
            else "Document"
        )
        if duration >= duration_limit:
            return await msg.edit(
                await gm(chat_id, "duration_limit_exceeded", [f"{duration_limit}"])
            )
        duration = str(td(seconds=duration)) if m.video else "Not Found"
        if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
            datas = {
                "user_id": user_id,
                "title": title,
                "duration": duration,
                "source_file": source_file,
                "link": link,
                "stream_type": "local_video",
            }
            await self.playlist.insert_one(chat_id, datas)

            msg = await msg.edit(await gm(chat_id, "added_to_playlist"))
            await asyncio.sleep(5)
            return await msg.delete()
        return await self._local_video_play(msg, title, duration, source_file, link)
