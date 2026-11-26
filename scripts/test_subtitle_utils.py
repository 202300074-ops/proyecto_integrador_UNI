import unittest

from scripts.subtitle_utils import build_srt


class BuildSrtTests(unittest.TestCase):
    def test_splits_long_scene_into_readable_cues_and_preserves_total_duration(self):
        result = build_srt(
            ["En Yucatán, algunas familias cuidan a la Xunáan Kaab en jobones."],
            [8.0],
            max_chars=24,
        )
        blocks = result.strip().split("\n\n")

        self.assertGreater(len(blocks), 1)
        self.assertIn("00:00:00,000 -->", blocks[0])
        self.assertIn("00:00:08,000", blocks[-1])
        self.assertTrue(all(len(line) <= 24 for block in blocks for line in block.splitlines()[2:]))

    def test_rejects_mismatched_or_non_positive_durations(self):
        with self.assertRaises(ValueError):
            build_srt(["Una escena"], [])
        with self.assertRaises(ValueError):
            build_srt(["Una escena"], [0])

    def test_accepts_two_scenes_with_contiguous_timing(self):
        result = build_srt(["Primera escena", "Segunda escena"], [2.0, 3.0])
        self.assertIn("00:00:00,000 --> 00:00:02,000", result)
        self.assertIn("00:00:02,000 --> 00:00:05,000", result)


if __name__ == "__main__":
    unittest.main()
