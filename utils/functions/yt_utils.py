import pafy
import requests
from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL as YtDL
from typing import Dict, List


def get_audio_direct_link(yt_url: str, audio_quality: str) -> str:
    if audio_quality.lower() == "low":
        with YoutubeDL({"format": "worstaudio"}) as yt_dls:
            info = yt_dls.extract_info(yt_url, download=False)
            return info["url"]
    elif audio_quality.lower() in ["medium", "high"]:
        with YoutubeDL({"format": "bestaudio"}) as yt_dls:
            info = yt_dls.extract_info(yt_url, download=False)
            return info["url"]


def get_video_direct_link(yt_url: str, video_quality: str):
    ydl = YtDL()
    ress = ydl.extract_info(yt_url, download=False)
    yt_res: List[Dict[str, str]] = []
    for res in ress["formats"]:
        if res["ext"] == "mp4":
            if (
                video_quality.lower() == "low"
                and res["format_note"] == "360p"
                and res["acodec"] != "none"
            ):
                rus = {"quality": res["format_note"], "direct_url": res["url"]}
                yt_res.append(rus.copy())
            if (
                video_quality.lower() == "medium"
                and res["format_note"] == "480p"
                and res["acodec"] != "none"
            ):
                rus = {"quality": res["format_note"], "direct_url": res["url"]}
                yt_res.append(rus.copy())
            if (
                video_quality.lower() == "high"
                and res["format_note"] == "720p"
                and res["acodec"] != "none"
            ):
                rus = {"quality": res["format_note"], "direct_url": res["url"]}
                yt_res.append(rus.copy())
            if not yt_res and (
                res["format_note"] == "720p"
                and res["acodec"] != "none"
            ):
                rus = {"quality": res["format_note"], "direct_url": res["url"]}
                yt_res.append(rus.copy())
    return yt_res[0]["direct_url"]


def download_yt_thumbnails(thumb_url, user_id):
    r = requests.get(thumb_url)
    with open(f"search/thumb{user_id}.jpg", "wb") as file:
        for chunk in r.iter_content(1024):
            file.write(chunk)
    return f"search/thumb{user_id}.jpg"


def format_count(number: int):
    num = float(f"{number:.3g}")
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return f"{str(num).rstrip('0').rstrip('.')}{['', 'K', 'M', 'B', 'T'][magnitude]}"


def get_yt_details(link: str):
    pufy = pafy.new(link)
    return {
        "thumbnails": pufy.bigthumbhd,
        "title": pufy.title,
        "duration": pufy.duration,
        "views": format_count(pufy.viewcount),
        "likes": format_count(pufy.likes),
        "dislikes": format_count(pufy.dislikes),
        "rating": round(pufy.rating, 2),
        "channel": pufy.author,
        "link": link
    }
