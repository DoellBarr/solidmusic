from pyrogram import filters

from solidmusic.core.client import Client
from solidmusic.core.types import Message
from solidmusic.database.lang_utils import gm
from solidmusic.functions.lyrcis_search import (
    parse_url,
    get_lyrics,
    get_title,
    get_artist_name,
)


@Client.on_message(filters.command("lyrics"))
async def _get_lyrics(_, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply("invalid_lyrics")
    query = "+".join(message.command[1:])
    lek = await message.reply("searching")
    google_link = f"https://google.com/search?q={query}+lyrics"
    parsed = await parse_url(google_link)
    lyrics, title, artist = (
        await get_lyrics(parsed),
        await get_title(parsed),
        await get_artist_name(parsed),
    )
    await lek.edit(await gm(chat_id, "lyrik", [title, artist, lyrics]))


__cmds__ = ["lyrics"]
__help__ = {"lyrics": "help_lyrics"}
