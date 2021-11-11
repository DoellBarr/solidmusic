from base.player import player
from sys import version
from os.path import exists
from os import mkdir
import asyncio

py_ver = version.split()[0]


def main():
    if not exists("search"):
        mkdir("search")
    if py_ver.startswith("3.9"):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(player.start())
    elif py_ver.startswith("3.10"):
        loop = asyncio.get_running_loop()
        loop.run_until_complete(player.start())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(player.start())


main()
