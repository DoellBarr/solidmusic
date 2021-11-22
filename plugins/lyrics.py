import requests
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import Message

from dB.lang_utils import get_message as gm

@Client.on_message(filters.command(["lyrics"]) & ~filters.edited)
async def lyrics(_, message : Message):
    if len(message.command) < 2:
        return await message.reply_text(gm(chid, "ly_key"))
    query = " ".join(message.command[1:])
    chid = message.chat.id
    lek = await message.reply_text(gm(chid, "searching"))
    req = requests.get(f"https://apis.xditya.me/lyrics?song={query}").json()
    lyric = req['lyrics']
    name = req['name']
    await lek.edit(gm(chid, "lyrik")).format({name},{lyric})
