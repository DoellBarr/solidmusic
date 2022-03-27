import json
from os.path import join, dirname, realpath
from os import listdir
from typing import Dict

from .chat_db import chat_db

lang_dir = join(dirname(realpath(__file__)), "lang")
list_lang = []
lang: Dict[str, Dict[str, str]] = {}

for file in listdir(lang_dir):
    if file.endswith(".json"):
        lang_code = file[:-5]
        list_lang.append(lang_code)
        lang[lang_code] = json.load(open(join(lang_dir, file), encoding="UTF-8"))


async def gm(chat_id: int, key: str, format_key=None) -> str:
    if not format_key:
        format_key = ["{}"]
    chat_lang = (await chat_db.get_chat(chat_id))["chat_lang"]
    return lang[chat_lang][key].format(*format_key)
