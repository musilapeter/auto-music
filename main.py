import threading
import time
import sys
import keyboard

from config import HOTKEY
from stt_listener import listen_and_transcribe
from intent_parser import parse_and_execute_intent

# Global lock to prevent overlapping voice capture sessions
is_listening = False
state_lock = threading.Lock()


def on_hotkey_triggered():
    """
    Callback function invoked when global hotkey is pressed.
    Runs listening & intent processing in a separate worker thread to avoid
    blocking the keyboard hook handler.
    """
    global is_listening

    with state_lock:
        if is_listening:
            print("[Main] Already listening or processing command. Please wait...")
            return
        is_listening = True

    # Spawn thread to handle audio capture and action execution asynchronously
    worker = threading.Thread(target=_process_voice_command, daemon=True)
    worker.start()


def _process_voice_command():
    global is_listening
    try:
        print("\n==========================================")
        print(f"[Main] Hotkey '{HOTKEY}' activated!")
        print("[Main] Listening for voice command...")

        # 1. Capture microphone audio & transcribe with Google STT
        transcribed_text = listen_and_transcribe()

        if transcribed_text:
            # 2. Parse intent and route to OS execution action
            success = parse_and_execute_intent(transcribed_text)
            if success:
                print("[Main] Action executed successfully.")
            else:
                print("[Main] Could not execute requested action.")
        else:
            print("[Main] No command recognized.")

        print("==========================================\n")
    except Exception as e:
        print(f"[Main] Error handling command: {e}")
    finally:
        with state_lock:
            is_listening = False


def main():
    print("==================================================")
    print(" Windows 11 Python Voice Desktop Assistant")
    print("==================================================")
    print(f"[*] Background Listener active.")
    print(f"[*] Global Trigger Shortcut: [{HOTKEY.upper()}]")
    print(f"[*] Idle CPU/RAM Usage: ~0%")
    print("[*] Press Ctrl+C in console to exit assistant.")
    print("==================================================")

    try:
        # Register global keyboard hook
        keyboard.add_hotkey(HOTKEY, on_hotkey_triggered, suppress=True)

        # Block main thread efficiently using system hooks (0% CPU idle)
        keyboard.wait()
    except KeyboardInterrupt:
        print("\n[Main] Assistant shut down by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Main] Fatal Error registering hotkey: {e}")
        print("[Hint] On Windows, 'keyboard' package may require Administrator/Elevated rights.")
        sys.exit(1)


if __name__ == "__main__":
    main()
