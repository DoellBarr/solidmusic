from yt_dlp import YoutubeDL
from typing import Dict, List

ydl = YoutubeDL()


def get_audio_direct_link(yt_url: str):
    ress = ydl.extract_info(yt_url, download=False)
    yt_res: List[Dict[str, str]] = []
    for res in ress["formats"]:
        if res["ext"] == "webm" and res["format_note"] == "medium":
            rus = {
                "quality": res["format_note"],
                "ext": res["ext"],
                "direct_url": res["url"],
            }
            yt_res.append(rus.copy())
    return yt_res[0]["direct_url"]


def get_video_direct_link(yt_url: str, video_quality: str):
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
