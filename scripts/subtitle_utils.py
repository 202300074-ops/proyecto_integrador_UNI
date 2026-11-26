"""Utilities for producing readable SRT subtitles from the narration script."""

from __future__ import annotations


def _wrap_lines(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        if len(word) > max_chars:
            raise ValueError("A word is longer than the subtitle line width.")
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
            continue
        lines.append(current)
        current = word

    if current:
        lines.append(current)
    return lines


def _timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    whole_seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{whole_seconds:02},{milliseconds:03}"


def build_srt(texts: list[str], durations: list[float], max_chars: int = 42) -> str:
    """Build two-line SRT cues, distributing each narration scene by text length."""
    if not texts or len(texts) != len(durations):
        raise ValueError("Texts and durations must have the same non-zero length.")
    if max_chars < 8:
        raise ValueError("Subtitle lines must allow at least eight characters.")
    if any(not text.strip() for text in texts):
        raise ValueError("Subtitle text cannot be empty.")
    if any(duration <= 0 for duration in durations):
        raise ValueError("Every subtitle scene must have positive duration.")

    cues: list[tuple[float, float, str]] = []
    elapsed = 0.0

    for text, duration in zip(texts, durations, strict=True):
        lines = _wrap_lines(text, max_chars)
        chunks = [lines[index:index + 2] for index in range(0, len(lines), 2)]
        weights = [sum(len(line) for line in chunk) for chunk in chunks]
        total_weight = sum(weights)
        cue_start = elapsed

        for index, (chunk, weight) in enumerate(zip(chunks, weights, strict=True)):
            cue_end = elapsed + duration if index == len(chunks) - 1 else cue_start + duration * weight / total_weight
            cues.append((cue_start, cue_end, "\n".join(chunk)))
            cue_start = cue_end

        elapsed += duration

    blocks = [
        f"{index}\n{_timestamp(start)} --> {_timestamp(end)}\n{text}"
        for index, (start, end, text) in enumerate(cues, start=1)
    ]
    return "\n\n".join(blocks) + "\n"
