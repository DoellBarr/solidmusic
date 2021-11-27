import time
from importlib import import_module
from os.path import join, dirname, realpath
from os import listdir
from typing import Dict, List

from pyrogram.types import InlineKeyboardButton

from database.lang_utils import get_message

plugins_dir = join(dirname(realpath(__file__)), ".")


cmds = {}
helps: Dict[str, Dict[str, str]] = {}
modules: List[InlineKeyboardButton] = []


def __all_module():
    for file in listdir(plugins_dir):
        if file.endswith(".py") and not file.startswith("__"):
            yield file[:-3]


def paginate_module(chat_id: int, user_id: int):
    global modules
    temp = []
    keyboard = []
    for count, button in enumerate(modules, start=1):
        temp.append(button)
        if count % 3 == 0:
            keyboard.append(temp)
            temp = []
        if len(modules) == count:
            keyboard.append(temp)
    keyboard.append(
        [
            InlineKeyboardButton(
                f"🗑️ {get_message(chat_id, 'close_btn_name')}", f"close|{user_id}"
            )
        ]
    )
    return keyboard


def load_module():
    for mods in __all_module():
        try:
            imported_mods = import_module(f"plugins.{mods}")
            time.sleep(0.25)
            print("|- Loaded Plugins " + imported_mods.__name__)
            if hasattr(imported_mods, "__cmds__"):
                if "_" in imported_mods.__name__:
                    x = imported_mods.__name__.split('_')[0]
                else:
                    x = imported_mods.__name__
                print(f"|- Loaded command {imported_mods.__cmds__}")
                cmds[x] = imported_mods.__cmds__
                modules.append(
                    InlineKeyboardButton(
                        x.split('plugins.')[1].title(),
                        callback_data=f"plugins.{mods.split('_')[0] if '_' in mods else mods}"
                    ))
            if hasattr(imported_mods, "__help__"):
                if "_" in imported_mods.__name__:
                    x = imported_mods.__name__.split('_')[0]
                else:
                    x = imported_mods.__name__
                helps[x] = imported_mods.__help__
        except SyntaxError as e:
            print(f"|- Not loaded {e.filename}\nBecause of {e.with_traceback(e.__traceback__)}")
