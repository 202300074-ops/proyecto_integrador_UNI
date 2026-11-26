import tempfile
import unittest
import wave
from array import array
from pathlib import Path

from scripts.audio_bed import write_original_music


class OriginalMusicTests(unittest.TestCase):
    def test_writes_bounded_pcm_with_requested_duration(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "music.wav"
            write_original_music(output, duration_seconds=0.5, sample_rate=8_000)

            with wave.open(str(output), "rb") as wav:
                self.assertEqual(wav.getnchannels(), 1)
                self.assertEqual(wav.getsampwidth(), 2)
                self.assertEqual(wav.getframerate(), 8_000)
                self.assertEqual(wav.getnframes(), 4_000)
                samples = array("h", wav.readframes(wav.getnframes()))
                self.assertGreater(max(abs(sample) for sample in samples), 0)
                self.assertLessEqual(max(abs(sample) for sample in samples), 32_767)

    def test_rejects_non_positive_duration_and_sample_rate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "music.wav"
            with self.assertRaises(ValueError):
                write_original_music(output, duration_seconds=0)
            with self.assertRaises(ValueError):
                write_original_music(output, duration_seconds=1, sample_rate=0)


if __name__ == "__main__":
    unittest.main()
