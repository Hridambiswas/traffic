import random
import subprocess
import yt_dlp

from config import CAMERA_SOURCES


def get_stream_url(youtube_url: str) -> str:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best[height<=480]/best",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info["url"]


def pick_source(sources: list[str] = CAMERA_SOURCES) -> str:
    order = sources[:]
    random.shuffle(order)
    for src in order:
        try:
            url = get_stream_url(src)
            print(f"[stream] connected: {src}")
            return url
        except Exception as e:
            print(f"[stream] skipping {src}: {e}")
    raise RuntimeError("No accessible camera source found.")
