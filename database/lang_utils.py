import json
from os import path, listdir

from pyrogram import emoji

from .chat_database import ChatDB

lang_folder = path.join(path.dirname(path.realpath(__file__)), "lang")
code = ""
kode = []
langs = {}
lang_flags = {
    "en": f"{emoji.FLAG_UNITED_STATES} English",
    "id": f"{emoji.FLAG_INDONESIA} Indonesia",
    "grl": f"{emoji.FLAG_INDONESIA} Girl",
    "jv": f"{emoji.FLAG_INDONESIA} Javanese",
    "su": f"{emoji.FLAG_INDONESIA} Sundanese",
    "pt": f"{emoji.FLAG_PORTUGAL} Portuguese",
    "ta": f"{emoji.FLAG_INDIA} Tamil",
    "hi": f"{emoji.FLAG_INDIA} Hindi",
    "mi": f"{emoji.FLAG_INDIA} Marathi",
}
db = ChatDB()
for file in listdir(lang_folder):
    if file.endswith(".json"):
        code = file[:-5]
        kode.append(code)
        langs[code] = json.load(open(path.join(lang_folder, file), encoding="UTF-8"))


def get_message(chat_id: int, key: str) -> str:
    try:
        return langs[db.get_chat(chat_id)[0]["lang"]][key]
    except (IndexError, KeyError):
        try:
            return langs["en"][key]
        except KeyError:
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
