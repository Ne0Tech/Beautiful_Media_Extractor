#!/usr/bin/env python3
"""
YouTube / YouTube Music Playlist Downloader
--------------------------------------------
Downloads your own YouTube or YouTube Music playlist as MP3 or MP4 files.

Requirements:
    pip install yt-dlp
    Install ffmpeg: https://ffmpeg.org/download.html
      - macOS:   brew install ffmpeg
      - Ubuntu:  sudo apt install ffmpeg
      - Windows: extract anywhere, set FFMPEG_DIR to the folder containing
                 ffmpeg.exe AND ffprobe.exe  e.g. r"C:\ffmpeg\bin"
"""

import yt_dlp
import os
import sys

# ── Mode options ──────────────────────────────────────────────────────────────
AUDIO = "audio"  # Downloads as MP3
VIDEO = "video"  # Downloads as MP4


# ─────────────────────────────────────────────────────────────────────────────


def validate_ffmpeg(ffmpeg_dir: str):
    """Check that both ffmpeg.exe and ffprobe.exe exist in the given folder."""
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
    return ffmpeg_dir


def build_audio_opts(output_dir: str, quality: str, ffmpeg_dir: str) -> dict:
    """yt-dlp options for MP3 audio download."""
    return {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            },
            {"key": "EmbedThumbnail"},  # Album art
            {"key": "FFmpegMetadata", "add_metadata": True},  # ID3 tags
        ],
        "outtmpl": os.path.join(output_dir, "%(artist)s - %(title)s.%(ext)s"),
        "writethumbnail": True,
        **({"ffmpeg_location": ffmpeg_dir} if ffmpeg_dir else {}),
    }


def build_video_opts(output_dir: str, quality: str, ffmpeg_dir: str) -> dict:
    """yt-dlp options for MP4 video download.

    Quality options:
        '2160'  → 4K
        '1440'  → 1440p
        '1080'  → 1080p (default)
        '720'   → 720p
        '480'   → 480p
    """
    # Try to get the requested resolution; fall back to the best available
    fmt = (
        f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]"
        f"/bestvideo[height<={quality}]+bestaudio"
        f"/best[height<={quality}]"
        f"/best"
    )
    return {
        "format": fmt,
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
            {"key": "FFmpegMetadata", "add_metadata": True},
        ],
        "outtmpl": os.path.join(output_dir, "%(uploader)s - %(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        **({"ffmpeg_location": ffmpeg_dir} if ffmpeg_dir else {}),
    }


def download_playlist(
        playlist_url: str,
        mode: str = AUDIO,
        output_dir: str = "downloads",
        quality: str = None,
        ffmpeg_dir: str = None,
):
    """
    Download a YouTube / YouTube Music playlist.

    Args:
        playlist_url:  URL of the playlist.
        mode:          AUDIO (mp3) or VIDEO (mp4).
        output_dir:    Folder to save files into.
        quality:       Audio: '128', '192', '320' kbps.
                       Video: '480', '720', '1080', '1440', '2160' (pixels).
        ffmpeg_dir:    Folder containing ffmpeg.exe + ffprobe.exe (Windows).
                       Leave as None on macOS/Linux.
    """
    if mode not in (AUDIO, VIDEO):
        print("ERROR: MODE must be 'audio' or 'video'.")
        sys.exit(1)

    # Default quality per mode
    if quality is None:
        quality = "192" if mode == AUDIO else "1080"

        # Validate ffmpeg on Windows
        if ffmpeg_dir:
            ffmpeg_dir = validate_ffmpeg(ffmpeg_dir)
            print("Using ffmpeg from: " + ffmpeg_dir)

    os.makedirs(output_dir, exist_ok=True)

    if mode == AUDIO:
        ydl_opts = build_audio_opts(output_dir, quality, ffmpeg_dir)
        print("Mode: MP3 audio | Quality: " + quality + " kbps")
    else:
        ydl_opts = build_video_opts(output_dir, quality, ffmpeg_dir)
        print("Mode: MP4 video | Max resolution: " + quality + "p")

    # Shared options
    ydl_opts.update({
        "ignoreerrors": True,  # Skip unavailable videos instead of stopping
        "noplaylist": False,  # Always download the full playlist
        "quiet": False,
        "no_warnings": False,
    })

    print("Saving to: " + os.path.abspath(output_dir))

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
            print("Download complete!")
        except yt_dlp.utils.DownloadError as e:
            print("Download error: " + str(e))
            sys.exit(1)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── Configuration — edit these values ────────────────────────────────────

    PLAYLIST_URL = "https://www.youtube.com/watch?v=sSsTR8qqDl4"

    # Choose mode: AUDIO (mp3) or VIDEO (mp4)
    MODE = VIDEO

    # Audio quality (kbps):     "128"  "192"  "320"
    # Video max resolution (p): "480"  "720"  "1080"  "1440"  "2160"
    QUALITY = "1080"  # This field is used for both audio and video modes.

    OUTPUT_DIR = "downloads"  # Where your files will end up and can be changed to another folder by changing the path.

    FFMPEG_DIR = "C:\Users\pedigzav001\Downloads\;"
    # ─────────────────────────────────────────────────────────────────────────

    if "YOUR_PLAYLIST_ID" in PLAYLIST_URL:
        print("  Please set PLAYLIST_URL to your actual playlist URL.")
        print("    Edit the PLAYLIST_URL variable near the bottom of this script.")
        sys.exit(0)

    download_playlist_as_mp3: (PLAYLIST_URL, OUTPUT_DIR, QUALITY, FFMPEG_DIR)

    FFMPEG_DIR = r"C:\Users\pedigzav001\Downloads\ffmpeg-8.1.tar.xz"  # Replace the text in this string with the file path to the ffmpeg file downloaded earlier
