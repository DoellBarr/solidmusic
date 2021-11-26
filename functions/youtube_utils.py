from typing import List, Dict

import requests
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

from core import username
from database.lang_utils import get_message as gm

new: Dict[int, List] = {}
old: Dict[int, List[List[Dict]]] = {}
global_search: Dict[int, List[VideosSearch]] = {}
stream_result: Dict[int, List[List[Dict]]] = {}
total_search: Dict[int, List] = {}


def get_audio_direct_link(yt_url: str) -> str:
    with YoutubeDL({"format": "ba*"}) as ydl:
        info = ydl.extract_info(yt_url, download=False)
        return info["url"]


def get_video_direct_link(yt_url: str) -> str:
    with YoutubeDL({"format": "best"}) as ydl:
        info = ydl.extract_info(yt_url, download=False)
        return info["url"]


def get_yt_details(yt_url: str):
    with YoutubeDL() as ydl:
        infos = ydl.extract_info(yt_url, download=False)
        result = {
            "title": infos["title"],
            "thumbnail": infos["thumbnail"],
            "duration": infos["duration_string"],
            "channel": f"[{infos['uploader']}]({infos['uploader_url']})",
            "rating": round(float(infos["average_rating"]), 2),
            "views": infos["view_count"],
            "likes": infos["like_count"],
            "dislikes": infos["dislike_count"],
            "link": yt_url,
        }
        return result


def append_new_results(chat_id: int, results: List, yt_res: List):
    new[chat_id] = []
    for res in results:
        rus = {
            "yt_id": res["id"],
            "yt_url": f"https://youtube.com/watch?v={res['id']}",
            "title": res["title"],
            "duration": res["duration"],
        }
        yt_res.append(rus.copy())
    new[chat_id].append(yt_res)


def append_to_music(chat_id: int, yt_res):
    temp = []
    stream_result[chat_id] = []
    for count, res in enumerate(yt_res, start=1):
        temp.append(res)
        if count % 5 == 0:
            stream_result[chat_id].append(temp)
            temp = []
        if count == len(yt_res):
            stream_result[chat_id].append(temp)


def yt_search(chat_id, title: str):
    total_search[chat_id] = []
    rez = VideosSearch(title, limit=5)
    results = rez.result()["result"]
    yt_res = []
    append_new_results(chat_id, results, yt_res)
    global_search[chat_id] = []
    global_search[chat_id].append(rez)
    append_to_music(chat_id, yt_res)
    return yt_res


def next_search(chat_id):
    try:
        old[chat_id].append(new[chat_id][0])
    except KeyError:
        old[chat_id] = []
        old[chat_id].append(new[chat_id][0])
    rez = global_search[chat_id][0]
    rez.next()
    yt_res = []
    results = rez.result()["result"]
    append_new_results(chat_id, results, yt_res)
    total_search[chat_id].append(yt_res)
    append_to_music(chat_id, yt_res)
    return yt_res[0]


def prev_search(chat_id: int):
    preev = len(total_search[chat_id]) - 1
    yt_res = old[chat_id][preev]
    append_to_music(chat_id, yt_res)


def extract_info(chat_id: int, result: Dict[int, List]):
    result_str = ""
    res = list(filter(None, result[chat_id]))
    for count, res in enumerate(res[0], start=1):
        title = res["title"]
        duration = res["duration"]
        more_info = f"https://t.me/{username}?start=ytinfo_{res['yt_id']}"
        result_str += f"""
{count}.
{gm(chat_id, 'yt_title')}: {title[:35] + '...' if len(title) >= 35 and not title.endswith(' ') else res['title']}
{gm(chat_id, 'duration')}: {duration}
[{gm(chat_id, 'more_info')}]({more_info})
"""
    return result_str


def download_yt_thumbnails(thumb_url, user_id):
    r = requests.get(thumb_url)
    with open(f"search/thumb{user_id}.jpg", "wb") as file:
        for chunk in r.iter_content(1024):
            file.write(chunk)
    return f"search/thumb{user_id}.jpg"
