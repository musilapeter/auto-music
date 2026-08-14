import os
from pathlib import Path

# Hotkey settings
# Note: 'alt+space' requires running with Administrator privileges on Windows for some global hooks,
# or running as standard elevated script.
HOTKEY = "alt+space"

# Default Windows Music directory: C:\Users\<Username>\Music
MUSIC_DIR = Path.home() / "Music"

# Supported media extensions
SUPPORTED_AUDIO_EXTS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".wma", ".ogg"}

# Speech recognition timeout settings (seconds)
LISTEN_TIMEOUT = 5        # Seconds to wait for user to start speaking
PHRASE_TIME_LIMIT = 7     # Max seconds to allow speaking
