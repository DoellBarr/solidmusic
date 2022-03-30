import asyncio


async def get_audio_direct_link(yt_url: str):
    proc = await asyncio.create_subprocess_exec(
        "youtube-dl",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "bestaudio",
        yt_url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return stdout.decode().strip()


async def get_video_direct_link(yt_url: str):
    proc = await asyncio.create_subprocess_exec(
        "youtube-dl",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "best",
        yt_url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return stdout.decode().strip()
