# Windows 11 Lightweight Voice Desktop Assistant

A production-ready, ultra-lightweight Python desktop assistant for Windows 11. It runs silently in the background with near **0% CPU and minimal RAM usage when idle**, activating only when you press a global keyboard shortcut (**`Alt + Space`**).

---

## Key Features

1. **Near 0% Idle Resource Usage**: No continuous background audio recording or speech polling loops. Listens strictly when triggered.
2. **Global Hotkey Trigger (`Alt + Space`)**: Instantly wake up the assistant from any application without focusing a console.
3. **Google Web Speech STT**: Uses Google's Web Speech API (`SpeechRecognition`) for accurate speech-to-text.
4. **Dual Microphone Engine**: Built-in support for `sounddevice` + `numpy` (pre-compiled wheels for Python 3.14+) and `PyAudio`, requiring **zero C++ compiler tools**.
5. **Core Automation Handlers**:
   - **Play Music**: Scans `C:\Users\<Username>\Music` and launches audio files (`.mp3`, `.wav`, `.flac`, `.m4a`, etc.) in the default Windows media player. Supports matching specific song names!
   - **Open VS Code**: Instantly opens Visual Studio Code via system command (`code`).
   - **Open Chrome & Search**: Extracts search queries from your voice command and launches Google Search directly in Chrome / default web browser.

---

## File Structure

- [`config.py`](file:///d:/hippo/config.py): Configuration constants (Hotkey `Alt+Space`, Music folder path, timeouts).
- [`stt_listener.py`](file:///d:/hippo/stt_listener.py): Microphone audio capture (with `sounddevice` fallback) and Google Web Speech transcription.
- [`actions.py`](file:///d:/hippo/actions.py): System handlers for Music playback (`os.startfile`), VS Code (`subprocess`), and Web Search (`webbrowser`).
- [`intent_parser.py`](file:///d:/hippo/intent_parser.py): Keyword & pattern matching logic to route spoken text to handlers.
- [`main.py`](file:///d:/hippo/main.py): Non-blocking background listener and console application entry point.
- [`main.pyw`](file:///d:/hippo/main.pyw): Windowless entry point for silent background operation.
- [`requirements.txt`](file:///d:/hippo/requirements.txt): Third-party pip package dependencies (`SpeechRecognition`, `sounddevice`, `numpy`, `keyboard`).

---

## Installation & Setup Instructions

### 1. Prerequisites
- **Windows 11**
- **Python 3.8+** (including Python 3.14+) installed and added to system `PATH`.
- Microphone connected and default audio input configured.

### 2. Install Dependencies

In your activated virtual environment (`venv`), run:

```powershell
pip install -r requirements.txt
```

> [!TIP]
> **No C++ Compiler Required**: `sounddevice` and `numpy` use pre-compiled wheels provided by PyPI, resolving `Microsoft Visual C++ 14.0 or greater is required` build errors!

---

## How to Run the Assistant

### Option A: Interactive Mode (Console Visible)
Best for testing voice commands and seeing debug logs:

```powershell
python main.py
```

### Option B: Silent Background Mode (No Console Window)
Runs completely hidden in the background:

```powershell
pythonw main.pyw
```

---

## Voice Commands Reference

Press **`Alt + Space`**, wait for the prompt, and speak:

| Intent | Spoken Example | Action |
| :--- | :--- | :--- |
| **Open VS Code** | *"open code"*, *"open vs code"*, *"vscode"* | Spawns `code` command |
| **Play Music** | *"play music"*, *"play song"* | Plays a random song from `C:\Users\<Username>\Music` |
| **Play Specific Song**| *"play moonlight"*, *"play track bohemian rhapsody"* | Plays matching song from `Music` folder |
| **Search Web** | *"search python 3.14 features"*, *"google quantum computing"* | Opens Chrome/default browser with Google Search |

---

## How to Run Automatically on Windows 11 Startup

To make the assistant run silently every time Windows boots:

1. Press `Win + R`, type `shell:startup`, and press **Enter** (opens your Startup folder).
2. Right-click inside the Startup folder -> **New** -> **Shortcut**.
3. Set the target location to your `pythonw.exe` and `main.pyw` script path:
   ```cmd
   "d:\hippo\venv\Scripts\pythonw.exe" "d:\hippo\main.pyw"
   ```
4. Name the shortcut **Voice Desktop Assistant** and click **Finish**.
