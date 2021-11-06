import json
import logging
from os import path, listdir

from pyrogram import emoji

from .chat_db import get_chat, add_chat

lang_folder = path.join(path.dirname(path.realpath(__file__)), "lang")
code = ""
kode = []
langs = {}
lang_flags = {
    "en": f"{emoji.FLAG_UNITED_STATES} English",
    "id": f"{emoji.FLAG_INDONESIA} Indonesia",
    "su": f"{emoji.FLAG_INDONESIA} Sundanese",
    "jv": f"{emoji.FLAG_INDONESIA} Javanese",
    "pt": f"{emoji.FLAG_PORTUGAL} Portuguese",
}

for file in listdir(lang_folder):
    if file.endswith(".json"):
        code = file[:-5]
        kode.append(code)
        langs[code] = json.load(
            open(path.join(lang_folder, file), encoding="UTF-8")
        )


def get_message(chat_id: int, key: str):
    try:
        return langs[get_chat(chat_id)[0]["lang"]][key]
    except KeyError:
        try:
            logging.info("Add your chat to database use /addchat command")
            return langs["en"][key]
        except KeyError:
            logging.error("Check your key, maybe it is coming from there")
            return f"`Error`:\n**can't get lang with key: {key}**"


def get_lang(lang: str = None):
    """
    Get details from one language if lang parameter is filled\n
    otherwise\n
    Get all available language in lang directory
    :param lang:
    :return: {key: value} | list[str]
    """
    if lang:
        return langs[lang]
    return kode
