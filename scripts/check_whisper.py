"""
Connectivity check for Whisper (OpenAI-compatible audio API).

Reads WHISPER_API_KEY and WHISPER_API_ENDPOINT from environment via
src/config/load_env.py auto-loader. Maps to OPENAI_* if needed and attempts
to transcribe a short local audio file provided as an argument.

Usage:
  PYTHONPATH=$PWD python scripts/check_whisper.py path/to/audio.wav

If the OpenAI client is not installed, credential presence is validated
and the script exits 0 with a skip message.
"""

import os
import sys
from pathlib import Path

from src.config.load_env import load_dotenv_if_present  # noqa: F401 (side effect)
from src.config import get_secret


def try_live_transcribe(audio_path: Path) -> tuple[bool, str]:
    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return False, "openai client not installed; skipping live call"

    try:
        client = OpenAI()
        with audio_path.open("rb") as f:
            # Some providers require model name; 'whisper-1' is common for compatibility.
            resp = client.audio.transcriptions.create(model="whisper-1", file=f)
        _ = getattr(resp, "text", None) or str(resp)
        return True, "whisper live transcription succeeded"
    except Exception as e:
        return False, f"whisper live call failed: {e}"


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("ERROR: provide path to a small audio file (wav/mp3)")
        return 2

    audio_path = Path(argv[0])
    if not audio_path.exists():
        print(f"ERROR: file not found: {audio_path}")
        return 2

    # Ensure secrets are present
    # If WHISPER_* not provided but OPENAI_* present, get_secret will fail unless OPENAI_API_KEY is set.
    api_key = os.getenv("WHISPER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: Missing required secret: WHISPER_API_KEY or OPENAI_API_KEY")
        return 1

    # Map to OpenAI-compatible env if not set
    os.environ.setdefault("OPENAI_API_KEY", api_key)
    base = os.getenv("WHISPER_API_ENDPOINT")
    if base and (base.startswith("http://") or base.startswith("https://")):
        os.environ.setdefault("OPENAI_BASE_URL", base)

    ok, msg = try_live_transcribe(audio_path)
    print(msg)
    return 0 if ok or "not installed" in msg else 1


if __name__ == "__main__":
    raise SystemExit(main())

