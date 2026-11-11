
import os
import yt_dlp


def download_video(url, folder):
    if "instagram.com/" not in url.lower():
        raise ValueError("Faqat Instagram link yuboring!")

    options = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(folder, "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
