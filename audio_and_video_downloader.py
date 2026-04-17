#!/usr/bin/env python3
import yt_dlp
import os
import sys


def validate_ffmpeg(ffmpeg_dir):
    ffmpeg_dir = os.path.abspath(ffmpeg_dir)
    missing = [
        exe for exe in ("ffmpeg.exe", "ffprobe.exe")
        if not os.path.isfile(os.path.join(ffmpeg_dir, exe))
    ]
    if missing:
        for exe in missing:
            print("ERROR: Could not find " + exe + " in: " + ffmpeg_dir)
        sys.exit(1)
    return ffmpeg_dir


def download_media(url, mode="mp3", output_dir="downloads", quality="192", ffmpeg_dir=None):
    if ffmpeg_dir is None:
        print("ERROR: FFMPEG_DIR must be set.")
        sys.exit(1)

    ffmpeg_dir = validate_ffmpeg(ffmpeg_dir)
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------
    # MP3 MODE (your original)
    # -------------------------
    if mode == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality,
                },
                {"key": "EmbedThumbnail"},
                {"key": "FFmpegMetadata", "add_metadata": True},
            ],
            "outtmpl": os.path.join(output_dir, "%(artist)s - %(title)s.%(ext)s"),
            "writethumbnail": True,
            "ffmpeg_location": ffmpeg_dir,
            "noplaylist": False,
        }

        print("Mode: MP3 | Quality:", quality, "kbps")

    # -------------------------
    # MP4 VIDEO MODE (NEW)
    # -------------------------
    elif mode == "mp4":
        ydl_opts = {
            "format": "bestvideo[height<=1080]+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "ffmpeg_location": ffmpeg_dir,
            "noplaylist": False,
        }

        print("Mode: MP4 Video")

    else:
        print("Invalid mode. Use 'mp3' or 'mp4'")
        sys.exit(1)

    print("Saving to:", os.path.abspath(output_dir))

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("Download complete!")
        except yt_dlp.utils.DownloadError as e:
            print("Download error:", str(e))
            sys.exit(1)


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":

    URL = "-------"

    MODE = "mp3"   #CHANGE THIS: "mp3" or "mp4"

    QUALITY = "192"

    OUTPUT_DIR = "downloads"

    FFMPEG_DIR = r"------"

    download_media(URL, MODE, OUTPUT_DIR, QUALITY, FFMPEG_DIR)
