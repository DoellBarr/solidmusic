from pyrogram import Client, filters
from pyrogram.types import Message

from database.lang_utils import get_message as gm
from functions.lyrics_search import get_lyrics, get_artist, get_title, parse_url


@Client.on_message(filters.command("lyrics"))
async def _get_lyrics(_, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply(gm(chat_id, "invalid_lyrics"))
    query = "+".join(message.command[1:])
    lek = await message.reply(gm(chat_id, "searching"))
    google_link = f"https://google.com/search?q={query}+lyrics"
    parsed = parse_url(google_link)
    lyrics, title, artist = get_lyrics(parsed), get_title(parsed), get_artist(parsed)
    await lek.edit(gm(chat_id, "lyrik").format(title, artist, lyrics))


__cmds__ = ["lyrics"]
__help__ = {
    "lyrics": "help_lyrics"
}
