import asyncio
from core.player import player
from os import path, mkdir


def main():
    if not path.exists("search"):
        mkdir("search")
    asyncio.run(player.run())


main()
