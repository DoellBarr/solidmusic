import asyncio
from core.player import player
from database.scaffold import Scaffold
from os import path, mkdir


def main():
    if not path.exists("search"):
        mkdir("search")
    Scaffold().init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(player.run())


main()
