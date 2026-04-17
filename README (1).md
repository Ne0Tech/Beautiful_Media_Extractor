# YouTube Music Playlist to MP3 Downloader

Downloads your own YouTube or YouTube Music playlists as MP3 files with album art and metadata.

## Requirements

- Python 3.7+
- yt-dlp: `pip install yt-dlp`
- ffmpeg: [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Setup

Edit the variables at the bottom of `audio_downloader.py`:

```python
PLAYLIST_URL = "https://music.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
QUALITY      = "192"          # "128", "192", or "320" kbps
OUTPUT_DIR   = "downloads"
FFMPEG_DIR   = r"C:\ffmpeg\bin"  # Windows: folder containing ffmpeg.exe and ffprobe.exe
                                  # macOS/Linux: set to None
```

Then run:

```bash
python audio_downloader.py
```

## Notes

- For downloading your own content only
- Unavailable tracks in a playlist are skipped automatically
