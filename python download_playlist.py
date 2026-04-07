#!/usr/bin/env python3
"""
YouTube Music Playlist to MP3 Downloader
-----------------------------------------
Downloads your own YouTube Music playlist tracks as MP3 files.

Requirements:
    pip install yt-dlp
    Install ffmpeg: https://ffmpeg.org/download.html
      - macOS:   brew install ffmpeg
      - Ubuntu:  sudo apt install ffmpeg
      - Windows: download from https://ffmpeg.org/download.html and extract anywhere.
                 Set FFMPEG_DIR below to the folder containing ffmpeg.exe AND ffprobe.exe.
                 e.g. r"C:\ffmpeg\bin"
                 Both ffmpeg.exe and ffprobe.exe must be in that same folder.
"""

import yt_dlp
import os
import sys


def download_playlist_as_mp3(
    playlist_url: str,
    output_dir: str = "downloads",
    audio_quality: str = "192",
    ffmpeg_dir: str = None,
):
    """
    Download a YouTube/YouTube Music playlist as MP3 files.

    Args:
        playlist_url:   URL of the YouTube or YouTube Music playlist.
        output_dir:     Folder where MP3s will be saved (created if missing).
        audio_quality:  Bitrate in kbps — '128', '192' (default), or '320'.
        ffmpeg_dir:     Folder containing ffmpeg.exe AND ffprobe.exe.
                        If None, assumes both are already in PATH.
    """

    # Validate ffmpeg + ffprobe are both present
    if ffmpeg_dir:
        ffmpeg_dir = os.path.abspath(ffmpeg_dir)
        missing = [
            exe for exe in ("ffmpeg.exe", "ffprobe.exe")
            if not os.path.isfile(os.path.join(ffmpeg_dir, exe))
        ]
        if missing:
            for exe in missing:
                print(f"❌  Could not find {exe} in: {ffmpeg_dir}", file=sys.stderr)
            print("    Make sure both ffmpeg.exe and ffprobe.exe are in that folder.", file=sys.stderr)
            print("    Download from: https://ffmpeg.org/download.html", file=sys.stderr)
            sys.exit(1)
        print(f"🔧  Using ffmpeg from: {ffmpeg_dir}")

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        # Point yt-dlp at the ffmpeg folder directly (no PATH needed)
        **({"ffmpeg_location": ffmpeg_dir} if ffmpeg_dir else {}),

        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": audio_quality,
            },
            {
                "key": "EmbedThumbnail",   # Embed thumbnail as album art
            },
            {
                "key": "FFmpegMetadata",   # Write ID3 tags
                "add_metadata": True,
            },
        ],

        # Saves as: downloads/Artist - Title.mp3
        "outtmpl": os.path.join(output_dir, "%(artist)s - %(title)s.%(ext)s"),

        "ignoreerrors": True,   # Skip unavailable tracks instead of stopping
        "noplaylist": False,    # Always download the full playlist
        "writethumbnail": True, # Required for EmbedThumbnail post-processor
        "quiet": False,
        "no_warnings": False,
    }

    print(f"📂  Saving MP3s to: {os.path.abspath(output_dir)}")
    print(f"🎵  Quality: {audio_quality} kbps\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
            print("\n✅  Download complete!")
        except yt_dlp.utils.DownloadError as e:
            print(f"\n❌  Download error: {e}", file=sys.stderr)
            sys.exit(1)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── Configuration — edit these values ────────────────────────────────────
    PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLHKKR0on2yraLsuVx7HDwIIEuSfcJwqiv"
    OUTPUT_DIR   = "downloads"      # Folder to save MP3s into
    QUALITY      = "192"            # Options: "128", "192", "320"

    # Windows: set this to the FOLDER containing both ffmpeg.exe and ffprobe.exe
    #   FFMPEG_DIR = r"C:\ffmpeg\bin"
    # macOS/Linux: leave as None
    FFMPEG_DIR   = None
    # ─────────────────────────────────────────────────────────────────────────

    if "YOUR_PLAYLIST_ID" in PLAYLIST_URL:
        print("⚠️  Please set PLAYLIST_URL to your actual playlist URL.")
        print("    Edit the PLAYLIST_URL variable near the bottom of this script.")
        sys.exit(0)

    download_playlist_as_mp3(PLAYLIST_URL, OUTPUT_DIR, QUALITY, FFMPEG_DIR)

    FFMPEG_DIR = r"C:\Users\pedigzav001\Downloads\ffmpeg-8.1.tar.xz"