"""Render a two-host script (lines starting with `MIA:` / `GEORGE:`) to an mp3 with Kokoro."""

import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

SR = 24000
LINE = re.compile(r"^(MIA|GEORGE):\s*(.+)$")


def parse_script(text: str) -> list[tuple[str, str]]:
    turns, bad = [], []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        m = LINE.match(raw.strip())
        if m:
            turns.append((m.group(1), m.group(2).strip()))
        else:
            bad.append(raw)
    if bad:
        raise ValueError(f"{len(bad)} script line(s) without a speaker, first: {bad[0][:80]!r}")
    if not turns:
        raise ValueError("script is empty")
    return turns


def render(turns: list[tuple[str, str]], voices: dict[str, tuple[str, str]], speed: float,
           model_dir: Path) -> np.ndarray:
    kokoro = Kokoro(str(model_dir / "kokoro-v1.0.onnx"), str(model_dir / "voices-v1.0.bin"))
    parts, prev = [], None
    for speaker, text in turns:
        voice, lang = voices[speaker]
        audio, _ = kokoro.create(text, voice=voice, speed=speed, lang=lang)
        # Short reactions follow quickly; a same-speaker topic switch gets a longer beat.
        gap = 0.7 if speaker == prev else (0.15 if len(text) < 40 else 0.3)
        if parts:
            parts.append(np.zeros(int(SR * gap), dtype=np.float32))
        parts.append(audio.astype(np.float32))
        prev = speaker
    return np.concatenate(parts)


def to_mp3(audio: np.ndarray, out_path: Path, bitrate: str, title: str, artist: str) -> float:
    wav = out_path.with_suffix(".wav")
    sf.write(wav, audio, SR)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-codec:a", "libmp3lame",
         "-b:a", bitrate, "-ac", "1", "-metadata", f"title={title}", "-metadata", f"artist={artist}",
         str(out_path)],
        check=True,
    )
    wav.unlink()
    return len(audio) / SR
