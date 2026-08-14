from typing import Optional
import speech_recognition as sr

from config import LISTEN_TIMEOUT, PHRASE_TIME_LIMIT

# Try importing sounddevice as high-level robust backend for Windows 11 without C compilers
try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False


def listen_and_transcribe() -> Optional[str]:
    """
    Captures short voice audio from the microphone after trigger and transcribes it
    using Google Web Speech API via SpeechRecognition.

    Supports PyAudio if available, and falls back to sounddevice for zero-compilation
    compatibility on Python 3.14+ on Windows.

    Returns:
        Transcribed string in lowercase, or None if transcription fails or speech was empty.
    """
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    audio_data = None

    # Strategy 1: Attempt PyAudio (standard SpeechRecognition microphone source)
    try:
        with sr.Microphone() as source:
            print("[STT] Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            print("[STT] Listening for voice command...")
            audio_data = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_TIME_LIMIT
            )
    except (AttributeError, OSError, ImportError) as mic_err:
        # Strategy 2: Fall back to sounddevice if PyAudio is missing/not compiled
        if HAS_SOUNDDEVICE:
            print(f"[STT] PyAudio not active ({mic_err}). Capturing via sounddevice...")
            try:
                samplerate = 16000
                duration = PHRASE_TIME_LIMIT
                print(f"[STT] Listening via sounddevice for {duration} seconds...")

                # Record mono int16 audio array
                recording = sd.rec(
                    int(duration * samplerate),
                    samplerate=samplerate,
                    channels=1,
                    dtype='int16'
                )
                sd.wait()  # Block until recording finishes

                raw_pcm_bytes = recording.tobytes()
                # 2 bytes per sample for int16
                audio_data = sr.AudioData(raw_pcm_bytes, samplerate, 2)
            except Exception as sd_err:
                print(f"[STT] sounddevice recording failed: {sd_err}")
                return None
        else:
            print("[STT] Neither PyAudio nor sounddevice is available.")
            return None

    if not audio_data:
        return None

    # Perform Google Web Speech STT
    try:
        print("[STT] Processing speech recognition with Google API...")
        text = recognizer.recognize_google(audio_data)
        clean_text = text.strip().lower()
        print(f"[STT] Heard: '{clean_text}'")
        return clean_text

    except sr.WaitTimeoutError:
        print("[STT] Listening timed out. No speech detected.")
        return None
    except sr.UnknownValueError:
        print("[STT] Speech was unintelligible or empty.")
        return None
    except sr.RequestError as e:
        print(f"[STT] Google Speech API request failed (Network dropout?): {e}")
        return None
    except Exception as e:
        print(f"[STT] Unexpected STT error: {e}")
        return None
