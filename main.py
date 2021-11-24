import asyncio
from core.player import player
from sys import version
from os import path, mkdir

py_ver = version.split()[0]


def main():
    if not path.exists("search"):
        mkdir("search")
    if py_ver.startswith("3.10"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(player.run())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(player.run())


main()
