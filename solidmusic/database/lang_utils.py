import yaml
from pyrogram import emoji

from solidmusic.database.chat_db import chat_db
from os.path import join, dirname, realpath
from os import listdir
from typing import Dict

lang_dir = join(dirname(realpath(__file__)), "langs")
list_lang = []
lang: Dict[str, Dict[str, str]] = {}
lang_flags = {
    "en": f"{emoji.FLAG_UNITED_STATES} English",
    "id": f"{emoji.FLAG_INDONESIA} Indonesia"
}

for file in listdir(lang_dir):
    if file.endswith(".yaml"):
        lang_code = file[:-5]
        list_lang.append(lang_code)
        lang[lang_code] = yaml.full_load(open(join(lang_dir, file)))


async def gm(chat_id: int, key: str, format_key=None) -> str:
    if not format_key:
        format_key = ["{}"]
    chat_lang = (await chat_db.get_chat(chat_id))["chat_lang"]
    return lang[chat_lang][key].format(*format_key)
