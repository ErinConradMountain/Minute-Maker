"""
Generate a short WAV file with a synthetic sine tone and optional speech-like envelope.

Usage:
  PYTHONPATH=$PWD python scripts/gen_sample_audio.py assets/sample.wav
"""

from __future__ import annotations

import math
import wave
from pathlib import Path


def generate_sine_wav(path: Path, seconds: float = 1.5, freq: float = 440.0, rate: int = 16000) -> None:
    n_frames = int(seconds * rate)
    amplitude = 0.25  # keep headroom

    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as wf:
        n_channels = 1
        sampwidth = 2  # 16-bit PCM
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(rate)

        frames = bytearray()
        for i in range(n_frames):
            t = i / rate
            # Simple amplitude envelope to avoid clicks
            env = min(1.0, t / 0.05) * min(1.0, (seconds - t) / 0.05)
            sample = amplitude * env * math.sin(2 * math.pi * freq * t)
            # Convert to 16-bit signed int
            val = max(-1.0, min(1.0, sample))
            ival = int(val * 32767)
            frames += int.to_bytes(ival & 0xFFFF, length=2, byteorder="little", signed=False)

        wf.writeframes(frames)


def main() -> int:
    import sys

    if len(sys.argv) < 2:
        print("Usage: python scripts/gen_sample_audio.py <output.wav>")
        return 2
    out = Path(sys.argv[1])
    generate_sine_wav(out)
    print(f"Wrote sample audio to {out.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

