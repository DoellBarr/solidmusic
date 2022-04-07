import asyncio
from solidmusic.core.player import player
from os import path, mkdir


async def main():
    if not path.exists("image"):
        mkdir("image")
    await player.run()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())