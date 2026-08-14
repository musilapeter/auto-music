import re
from typing import Tuple, Optional

from actions import play_music, open_vscode, search_web


def parse_and_execute_intent(text: str) -> bool:
    """
    Parses transcribed text to determine the user intent and routes it
    to the appropriate OS execution handler.

    Supported Intents:
    1. Open VS Code ('open code', 'vs code', 'vscode', etc.)
    2. Play Music ('play music', 'play song', 'play <song_name>')
    3. Search Web ('search <query>', 'google <query>', 'look up <query>')
    """
    if not text:
        return False

    clean_text = text.strip().lower()

    # 1. VS Code Intent
    vscode_triggers = ["open vs code", "open vscode", "open code", "launch code", "vs code", "vscode"]
    if any(trigger in clean_text for trigger in vscode_triggers):
        return open_vscode()

    # 2. Music Intent
    if "play" in clean_text or "music" in clean_text or "song" in clean_text:
        song_query = _extract_song_query(clean_text)
        return play_music(song_query=song_query)

    # 3. Web Search Intent
    search_triggers = ["search", "google", "find", "look up", "browse"]
    if any(trigger in clean_text for trigger in search_triggers):
        query = _extract_search_query(clean_text)
        if query:
            return search_web(query)
        else:
            print("[Intent] Search trigger detected but no query extracted.")
            return False

    # Fallback / Default: Treat unhandled phrases as a Google web search
    print(f"[Intent] Unmatched intent pattern. Defaulting to web search for: '{clean_text}'")
    return search_web(clean_text)


def _extract_song_query(text: str) -> Optional[str]:
    """
    Extracts song query from phrase like 'play moonlight' or 'play music track'.
    """
    # Remove phrases like 'play music', 'play song', 'play'
    patterns = [
        r"^play\s+music\s+for\s+",
        r"^play\s+music\s+",
        r"^play\s+song\s+",
        r"^play\s+track\s+",
        r"^play\s+",
        r"\s+music$",
        r"\s+song$"
    ]
    query = text
    for pattern in patterns:
        query = re.sub(pattern, "", query, flags=re.IGNORECASE).strip()

    if query in ["", "music", "song", "a song", "some music"]:
        return None
    return query


def _extract_search_query(text: str) -> str:
    """
    Extracts search query from text like 'search for python 3' or 'google machine learning'.
    """
    patterns = [
        r"^(search\s+for\s+on\s+google\s+)",
        r"^(search\s+for\s+)",
        r"^(search\s+on\s+google\s+for\s+)",
        r"^(search\s+)",
        r"^(google\s+)",
        r"^(look\s+up\s+)",
        r"^(find\s+)"
    ]
    query = text
    for pattern in patterns:
        query = re.sub(pattern, "", query, flags=re.IGNORECASE).strip()
    return query
