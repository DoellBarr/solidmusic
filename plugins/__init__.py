import time
from importlib import import_module
from os.path import join, dirname, realpath
from os import listdir

plugins_dir = join(dirname(realpath(__file__)), ".")


def __all_module():
    global plugins_dir
    for file in listdir(plugins_dir):
        if file.endswith(".py") and not file.startswith("__"):
            yield file[:-3]


def load_module():
    for mods in __all_module():
        try:
            imported_mods = import_module(f"plugins.{mods}")
            time.sleep(1)
            print("|- Loaded " + imported_mods.__name__)
        except SyntaxError as e:
            print(f"|- Not loaded {e.filename}\nBecause of {e.with_traceback(e.__traceback__)}")

