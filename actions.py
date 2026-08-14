import os
import random
import subprocess
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Optional

from config import MUSIC_DIR, SUPPORTED_AUDIO_EXTS


def play_music(song_query: Optional[str] = None) -> bool:
    """
    Scans the user's default Windows Music folder, selects a matching audio file
    (or a random/first audio file if no query/match is found), and launches it
    using the system's default media player application.
    """
    if not MUSIC_DIR.exists():
        print(f"[Actions] Music directory does not exist: {MUSIC_DIR}")
        return False

    # Find all supported audio files recursively in Music directory
    audio_files = [
        p for p in MUSIC_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_AUDIO_EXTS
    ]

    if not audio_files:
        print(f"[Actions] No audio files found in: {MUSIC_DIR}")
        return False

    target_file = None

    if song_query:
        query_clean = song_query.strip().lower()
        # Find matches where query words appear in file stem/name
        matching_files = [
            f for f in audio_files
            if query_clean in f.stem.lower() or query_clean in f.name.lower()
        ]
        if matching_files:
            target_file = matching_files[0]
            print(f"[Actions] Found matching song for '{song_query}': {target_file.name}")

    if not target_file:
        # Pick a random audio file if no query match or no query specified
        target_file = random.choice(audio_files)
        print(f"[Actions] Playing music: {target_file.name}")

    try:
        # os.startfile is Windows-native and launches the file with default associated player
        os.startfile(str(target_file))
        return True
    except Exception as e:
        print(f"[Actions] Error playing music file '{target_file}': {e}")
        return False


def open_vscode() -> bool:
    """
    Launches Visual Studio Code using the system shell command ('code').
    """
    try:
        print("[Actions] Opening Visual Studio Code...")
        subprocess.Popen(["code"], shell=True)
        return True
    except Exception as e:
        print(f"[Actions] Failed to launch VS Code: {e}")
        return False


def search_web(query: str) -> bool:
    """
    Parses search query and opens Google Chrome / system default browser
    directly to the Google search results page.
    """
    if not query or not query.strip():
        print("[Actions] Empty search query provided.")
        return False

    clean_query = query.strip()
    encoded_query = urllib.parse.quote(clean_query)
    search_url = f"https://www.google.com/search?q={encoded_query}"

    try:
        print(f"[Actions] Searching web for: '{clean_query}'")
        webbrowser.open(search_url)
        return True
    except Exception as e:
        print(f"[Actions] Error opening browser: {e}")
        return False
