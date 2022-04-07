import time
from importlib import import_module
from os.path import join, dirname, realpath
from os import listdir
from pyrogram.types import InlineKeyboardButton

from solidmusic.database.lang_utils import gm

plugins_dir = join(dirname(realpath(__file__)), ".")
cmds = {}
helps: dict[str, dict[str, str]] = {}
modules: list[InlineKeyboardButton] = []


def __all_module():
    for file in listdir(plugins_dir):
        if file.endswith(".py") and not file.startswith("__"):
            yield file[:-3]


def paginate_module(chat_id: int, user_id: int):
    temp, keyboard = [], []
    for count, btn in enumerate(modules, start=1):
        temp.append(btn)
        if count % 3 == 0:
            keyboard.append(temp)
            temp = []
        if len(modules) == count:
            keyboard.append(temp)
    keyboard.append(
        [
            InlineKeyboardButton(f"⬅️ {await gm(chat_id, 'backtomenu')}", "goback"),
            InlineKeyboardButton(
                f"🗑️ {await gm(chat_id, 'close_btn_name')}", f"close|{user_id}"
            ),
        ]
    )
    temp.clear()
    return keyboard


def load_module(user_id: int | None = 0):
    for mods in __all_module():
        try:
            imported_module = import_module(f"solidmusic.plugins.{mods}")
            if not user_id:
                time.sleep(0.2)
                print(f"Loaded Plugins {imported_module.__name__}")
            if hasattr(imported_module, "__cmds__"):
                x = imported_module.__name__.split("_")[0]
                if not user_id:
                    print(f"Loaded Command {imported_module.__cmds__}")
                cmds[x] = imported_module.__cmds__
                if user_id:
                    modules.append(
                        InlineKeyboardButton(
                            x.split("solidmusic.plugins.")[1].title(),
                            callback_data=f"solidmusic.plugins.{mods.split('_')[0]}|{user_id}",
                        )
                    )
            if hasattr(imported_module, "__help__"):
                x = imported_module.__name__.split("_")[0]
                helps[x] = imported_module.__help__
        except SyntaxError as e:
            print(
                f"Not Loaded {e.filename}\nBecause of {e.with_traceback(e.__traceback__)}"
            )
