from base.player import player
from sys import version
import asyncio

py_ver = version.split()[0]


def main():
    if py_ver.startswith("3.9"):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(player.start())
    elif py_ver.startswith("3.10"):
        loop = asyncio.get_running_loop()
        loop.run_until_complete(player.start())


main()
