"""Create a soft, original ambient music bed using standard-library PCM tools."""

from __future__ import annotations

import math
import wave
from array import array
from pathlib import Path


CHORDS = (
    (146.83, 220.00, 293.66),
    (164.81, 246.94, 329.63),
    (130.81, 196.00, 261.63),
    (146.83, 220.00, 293.66),
)
MELODY = (293.66, 329.63, 392.00, 440.00, 392.00, 329.63, 293.66, 220.00)
CHORD_SECONDS = 8.0
NOTE_SECONDS = 2.0


def _sample_at(time_seconds: float, duration_seconds: float) -> float:
    chord = CHORDS[int(time_seconds // CHORD_SECONDS) % len(CHORDS)]
    chord_phase = 2 * math.pi * time_seconds
    pad = (
        math.sin(chord_phase * chord[0])
        + 0.55 * math.sin(chord_phase * chord[1] + 0.6)
        + 0.3 * math.sin(chord_phase * chord[2] + 1.1)
    ) / 1.85

    note_position = time_seconds % (NOTE_SECONDS * len(MELODY))
    note_index = int(note_position // NOTE_SECONDS)
    note_time = note_position % NOTE_SECONDS
    note_envelope = math.exp(-2.4 * note_time)
    note_phase = 2 * math.pi * MELODY[note_index] * note_time
    note = note_envelope * (math.sin(note_phase) + 0.14 * math.sin(note_phase * 2)) * 0.34

    fade_in = min(1.0, time_seconds / 1.5)
    fade_out = min(1.0, max(0.0, duration_seconds - time_seconds) / 2.0)
    return (pad * 0.16 + note * 0.22) * fade_in * fade_out


def write_original_music(
    output_path: Path,
    duration_seconds: float,
    sample_rate: int = 22_050,
) -> Path:
    """Write a quiet monophonic ambient cue; no external samples or licenses."""
    if duration_seconds <= 0:
        raise ValueError("Music duration must be positive.")
    if sample_rate < 8_000:
        raise ValueError("Sample rate must be at least 8 kHz.")

    frame_count = round(duration_seconds * sample_rate)
    samples = array(
        "h",
        (
            round(_sample_at(index / sample_rate, duration_seconds) * 32_767)
            for index in range(frame_count)
        ),
    )
    if samples.itemsize != 2:
        raise RuntimeError("This platform does not support 16-bit PCM samples.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(samples.tobytes())
    return path
