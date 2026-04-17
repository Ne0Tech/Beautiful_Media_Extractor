#!/usr/bin/env python3
"""
YouTube / YouTube Music Playlist to MP3 Downloader
"""

import yt_dlp
import os
import sys


def validate_ffmpeg(ffmpeg_dir):
    """Check that both ffmpeg.exe and ffprobe.exe exist in the given folder."""
    ffmpeg_dir = os.path.abspath(ffmpeg_dir)
    missing = [
        exe for exe in ("ffmpeg.exe", "ffprobe.exe")
        if not os.path.isfile(os.path.join(ffmpeg_dir, exe))
    ]
    if missing:
        for exe in missing:
            print("ERROR: Could not find " + exe + " in: " + ffmpeg_dir)
        print("Make sure both ffmpeg.exe and ffprobe.exe are in that folder.")
        print("Download from: https://ffmpeg.org/download.html")
        sys.exit(1)
    return ffmpeg_dir


def download_playlist_as_mp3(playlist_url, output_dir="downloads", quality="192", ffmpeg_dir=None):
    """
    Download a YouTube or YouTube Music playlist as MP3 files.

    Args:
        playlist_url:  URL of the playlist.
        output_dir:    Folder to save MP3s into.
        quality:       Bitrate in kbps - '128', '192' (default), or '320'.
        ffmpeg_dir:    Folder containing ffmpeg.exe and ffprobe.exe (Windows).
                       Leave as None on macOS/Linux.
    """
    if ffmpeg_dir is None:
        print("ERROR: FFMPEG_DIR must be set for MP3 conversion.")
        print("Set FFMPEG_DIR to the folder containing ffmpeg.exe and ffprobe.exe.")
        print("Download ffmpeg from: https://ffmpeg.org/download.html")
        sys.exit(1)

    ffmpeg_dir = validate_ffmpeg(ffmpeg_dir)
    print("Using ffmpeg from: " + ffmpeg_dir)

    os.makedirs(output_dir, exist_ok=True)

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
        "ignoreerrors": True,
        "noplaylist": False,
        "quiet": False,
        "no_warnings": False,
    }

    print("Mode: MP3 audio | Quality: " + quality + " kbps")
    print("Saving to: " + os.path.abspath(output_dir))

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
            print("Download complete!")
        except yt_dlp.utils.DownloadError as e:
            print("Download error: " + str(e))
            sys.exit(1)


# Entry point

if __name__ == "__main__":
    # --- Configuration: edit these values ---

    PLAYLIST_URL = "------"

    # Audio quality in kbps: "128", "192", or "320"
    QUALITY = "192"

    OUTPUT_DIR = "downloads"

    # Path to the folder containing ffmpeg.exe and ffprobe.exe
    #   e.g. FFMPEG_DIR = r"C:\ffmpeg\bin"
    FFMPEG_DIR = r"------"

    # ----------------------------------------

    if "YOUR_PLAYLIST_ID" in PLAYLIST_URL:
        print("Please set PLAYLIST_URL to your actual playlist URL.")
        print("Edit the PLAYLIST_URL variable near the bottom of this script.")
        sys.exit(0)

    download_playlist_as_mp3(PLAYLIST_URL, OUTPUT_DIR, QUALITY, FFMPEG_DIR)