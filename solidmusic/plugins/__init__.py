import glob
import time
from importlib import import_module
from os.path import join, dirname, realpath, basename, isfile
from os import listdir
from pyrogram.types import InlineKeyboardButton

from solidmusic.database.lang_utils import gm

plugins_dir = join(dirname(realpath(__file__)), ".")
cmds = {}
helps: dict[str, dict[str, str]] = {}
modules: list[InlineKeyboardButton] = []


async def paginate_module(chat_id: int, user_id: int):
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
    mod_paths = glob.glob(f"{dirname(__file__)}/*.py")
    all_modules = sorted(
        [
            basename(f)[:-3]
            for f in mod_paths
            if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
        ]
    )
    for mods in all_modules:
        try:
            imported_module = import_module(f"solidmusic.plugins.{mods}")
            if hasattr(imported_module, "__cmds__"):
                x = imported_module.__name__.split("_")[0]
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
