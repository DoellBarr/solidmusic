from pyrogram import filters

from solidmusic.core import types
from solidmusic.core.client import Client
from solidmusic.core.player import player
from solidmusic.database.lang_utils import gm
from solidmusic.functions.decorators import authorized_only


@Client.on_message(filters.command("playlist"))
@authorized_only
async def playlist_(client: Client, message: types.Message):
    bot_username = (await client.get_me()).username
    chat_id = message.chat.id
    current, queued = await player.send_playlist(chat_id)
    if current and not queued:
        current_title = current["title"]
        current_stream_type = current["stream_type"]
        current_yt_info = (
            f"https://t.me/{bot_username}?start=ytinfo_{current['yt_id']}"
            if current_stream_type in ["video", "music"]
            else current["link"]
        )
        text = f"**{await gm(chat_id, 'now_streaming')}**:\n» [{current_title}]({current_yt_info}) | `{current_stream_type}`"
        return await message.reply_text(text, disable_web_page_preview=True)
    if current:
        current_title = current["title"]
        current_stream_type = current["stream_type"]
        current_yt_info = (
            f"https://t.me/{bot_username}?start=ytinfo_{current['yt_id']}"
            if current_stream_type in ["video", "music"]
            else current["link"]
        )
        text = (
            f"**{await gm(chat_id, 'now_streaming')}**:\n» [{current_title}]({current_yt_info}) | `{current_stream_type}`\n\n"
            f"**{await gm(chat_id, 'playlist')}**\n"
        )
        for count, queues in enumerate(queued, start=1):
            queue_title = queues["title"]
            queue_stream_type = queues["stream_type"]
            queue_yt_info = (
                f"https://t.me/{bot_username}?start=ytinfo_{queues['yt_id']}"
                if queue_stream_type in ["video", "music"]
                else queues["link"]
            )
            text += f"**#{count}** - [{queue_title}]({queue_yt_info}) | `{queue_stream_type}`\n"
        return await message.reply_text(text, disable_web_page_preview=True)
    return await message.reply("no_playlists")


__cmds__ = ["playlist"]
__help__ = {
    "playlist": "help_playlist"
}
