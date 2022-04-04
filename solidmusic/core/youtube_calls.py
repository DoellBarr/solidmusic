from asyncio import sleep

from pyrogram.errors import FloodWait, UserNotParticipant

from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped

from solidmusic.core.types import CallbackQuery
from solidmusic.functions.yt_utils import get_audio_direct_link, get_video_direct_link
from solidmusic.database.lang_utils import gm
from solidmusic.core.calls import Call


class YoutubePlayer(Call):
    async def stream(
        self,
        cb: CallbackQuery,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
        stream_type: str
    ):
        m = cb.message
        bot_username = await self.bot.get_username()
        mention = await m.from_user.mention
        user_id = m.from_user.id
        chat_id = m.chat.id
        call = self.call
        playlist = self.playlist.playlist
        if playlist and chat_id not in playlist or not playlist:
            await self.init_youtube_player(
                chat_id, user_id, title, duration, yt_url, yt_id, stream_type
            )
        elif playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
            await self.init_youtube_player(
                chat_id, user_id, title, duration, yt_url, yt_id, stream_type
            )
            mess = await cb.edit("track_queued")
            await sleep(5)
            return await mess.delete()
        audio_parameters, video_parameters = await self.get_quality(chat_id)
        path = await get_audio_direct_link(yt_url) if stream_type == "audio" else await get_video_direct_link(yt_url)
        stream_type_text = "stream_type_youtube_audio" if stream_type == "audio" else "stream_type_youtube_video"
        stream = (
            AudioPiped(path, audio_parameters)
            if stream_type == "audio"
            else AudioVideoPiped(path, audio_parameters, video_parameters)
        )
        msg = await cb.edit("process")
        try:
            await call.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
            return await msg.edit(
                f"""
{await gm(chat_id, 'now_streaming')}
{await gm(chat_id, 'yt_title')}: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})
{await gm(chat_id, 'duration')}: {duration}
{await gm(chat_id, 'req_by')}: {mention}
{await gm(chat_id, 'stream_type_tite')}: {await gm(chat_id, stream_type_text)}
""",
                disable_web_page_preview=True
            )
        except NoActiveGroupCall:
            await self.join_chat(m)
            await self.start_call(m)
            return await self.stream(
                cb, title, duration, yt_url, yt_id, stream_type
            )
        except FloodWait as x:
            await msg.edit(await gm(chat_id, "error_flood", [f"{x.x}"]))
            await sleep(x.x)
            return await self.stream(
                cb, title, duration, yt_url, yt_id, stream_type
            )
        except UserNotParticipant:
            await self.join_chat(m)
            return await self.stream(
                cb, title, duration, yt_url, yt_id, stream_type
            )
