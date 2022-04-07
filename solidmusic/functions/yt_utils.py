from youtubesearchpython.__future__ import VideosSearch
import asyncio
import json
import aiofiles
from aiohttp import ClientSession
from datetime import timedelta as td
import solidmusic.core
from solidmusic.database.lang_utils import gm

s = ClientSession
new: dict[int, list] = {}
old: dict[int, list[list[dict]]] = {}
global_search: dict[int, list[VideosSearch]] = {}
stream_result: dict[int, list[list[dict]]] = {}
total_search: dict[int, list] = {}


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


async def get_yt_details(yt_url: str):
    proc = await asyncio.create_subprocess_exec(
        "youtube-dl",
        "-j",
        "--skip-download",
        yt_url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    infos = stdout.decode().strip()
    data = json.loads(infos)
    rating = None if data["average_rating"] is None else data["average_rating"]
    return {
        "title": data["title"],
        "thumbnail": data["thumbnail"],
        "duration": str(td(seconds=data["duration"])),
        "channel": f"{data['uploader']} ({data['uploader_url']})",
        "views": data["view_count"],
        "likes": data["like_count"],
        "rating": rating,
        "link": yt_url
    }


def append_new_results(chat_id: int, results: list, yt_res: list):
    new[chat_id] = []
    for res in results:
        data = {
            "yt_id": res["id"],
            "yt_url": res["link"],
            "title": res["title"],
            "duration": res["duration"],
        }
        yt_res.append(data.copy())
    new[chat_id].append(yt_res)


def append_to_music(chat_id: int, yt_res: list):
    temp = []
    stream_result[chat_id] = []
    for count, res in enumerate(yt_res, start=1):
        temp.append(res)
        if count % 5 == 0:
            stream_result[chat_id].append(temp.copy())
            temp = []
        if count == len(yt_res):
            stream_result[chat_id].append(temp.copy())


async def yt_search(chat_id: int, title: str):
    total_search[chat_id] = []
    yt_res = []
    result = (VideosSearch(title, limit=5)).result().get("result")
    append_new_results(chat_id, result, yt_res)
    global_search[chat_id] = [result]
    append_to_music(chat_id, yt_res)
    return yt_res


async def next_search(chat_id: int):
    if chat_id not in old:
        old[chat_id] = []
    old[chat_id].append(new[chat_id][0])
    result = global_search[chat_id][0]
    await result.next()
    yt_res = []
    results = result.result()["result"]
    append_new_results(chat_id, results, yt_res)
    total_search[chat_id].append(yt_res)
    append_to_music(chat_id, yt_res)
    return yt_res[0]


def prev_search(chat_id: int):
    prev = len(total_search[chat_id]) - 1
    yt_res = old[chat_id][prev]
    append_to_music(chat_id, yt_res)


async def extract_info(chat_id: int, result: dict[int, list]):
    result_str = ""
    results = list(filter(None, result[chat_id]))
    for count, res in enumerate(results[0], start=1):
        title = res["title"]
        duration = res["duration"]
        more_info = f"https://t.me/{solidmusic.core.username}?start=ytinfo_{res['yt_id']}"
        result_str += f"""
    {count}.
    {await gm(chat_id, 'yt_title')}: {title[:35] + '...' if len(title) >= 35 and not title.endswith(' ') else res['title']}
    {await gm(chat_id, 'duration')}: {duration}
    [{await gm(chat_id, 'more_info')}]({more_info})
    """
    return result_str


async def download_yt_thumbnails(thumb_url: str, user_id: int):
    async with s() as ses, ses.get(thumb_url) as res:
        f = await aiofiles.open(f"image/{user_id}.jpg", mode="wb")
        await f.write(await res.read())
        await f.close()
    return f"image/{user_id}.jpg"
