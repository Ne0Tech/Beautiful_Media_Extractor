# YouTube Music Playlist to MP3 Downloader

A simple Python script that downloads your own YouTube or YouTube Music playlists as MP3 files, complete with album art and metadata tags.

---

## Requirements

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/download.html) (required for MP3 conversion)

---

## Installation

**1. Install yt-dlp**
```bash
pip install yt-dlp
```

**2. Install ffmpeg**

| OS | Command |
|----|---------|
| Windows | Download from [ffmpeg.org](https://ffmpeg.org/download.html) and extract to a folder e.g. `C:\ffmpeg` |
| macOS | `brew install ffmpeg` |
| Ubuntu/Debian | `sudo apt install ffmpeg` |

> **Windows users:** After extracting, make sure your folder contains both `ffmpeg.exe` and `ffprobe.exe`. You will point the script directly at this folder — no need to add anything to PATH.

---

## Usage

Open `audio_downloader.py` and edit the configuration variables near the bottom of the file:

```python
# URL of your YouTube or YouTube Music playlist
PLAYLIST_URL = "https://music.youtube.com/playlist?list=YOUR_PLAYLIST_ID"

# Audio quality in kbps: "128", "192", or "320"
QUALITY = "192"

# Folder to save MP3s into
OUTPUT_DIR = "downloads"

# Path to the folder containing ffmpeg.exe and ffprobe.exe (Windows)
# macOS/Linux: change to None if ffmpeg was installed via brew or apt
FFMPEG_DIR = r"C:\ffmpeg\bin"
```

Then run the script:

```bash
python audio_downloader.py
```

MP3 files will be saved to the `downloads` folder (or whatever you set `OUTPUT_DIR` to).

---

## Output

Files are saved in the following format:

```
downloads/
    Artist - Track Title.mp3
    Artist - Track Title.mp3
    ...
```

Each MP3 includes:
- Album art embedded as cover art
- ID3 metadata tags (title, artist, album, etc.)

---

## Configuration Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `PLAYLIST_URL` | Full URL of your YouTube/YT Music playlist | *(required)* |
| `QUALITY` | MP3 bitrate: `"128"`, `"192"`, or `"320"` | `"192"` |
| `OUTPUT_DIR` | Folder to save downloaded MP3s | `"downloads"` |
| `FFMPEG_DIR` | Path to folder containing `ffmpeg.exe` and `ffprobe.exe` | *(required on Windows)* |

---

## Notes

- This script is intended for downloading **your own content** from YouTube. Downloading copyrighted content you do not own may violate YouTube's Terms of Service.
- Unavailable videos in a playlist are skipped automatically.
- Requires an active internet connection.

---

## Dependencies

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube download library
- [ffmpeg](https://ffmpeg.org/) — Audio conversion and metadata embedding
