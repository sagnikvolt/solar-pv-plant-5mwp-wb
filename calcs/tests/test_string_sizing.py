import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from string_sizing import size_strings, temp_adjust, cell_temp_noct  # noqa: E402

EXAMPLE = os.path.join(os.path.dirname(__file__), "..", "config", "example_inputs.json")


class TestStringSizing(unittest.TestCase):
    def setUp(self):
        with open(EXAMPLE, encoding="utf-8") as f:
            self.cfg = json.load(f)

    def test_temp_adjust_at_stc_is_identity(self):
        self.assertAlmostEqual(temp_adjust(49.8, -0.27, 25), 49.8)

    def test_voc_rises_when_cold(self):
        self.assertGreater(temp_adjust(49.8, -0.27, 0), 49.8)

    def test_noct_model(self):
        # 45 °C ambient, NOCT 45 → 45 + 25/800*1000 = 76.25 °C
        self.assertAlmostEqual(cell_temp_noct(45, 45), 76.25)

    def test_example_hand_calc(self):
        r = size_strings(self.cfg)
        # Voc at 3 °C = 49.8 * (1 + 0.0027*22) = 52.758 V → floor(1500/52.758) = 28
        self.assertAlmostEqual(r["Voc_cold_V"], 52.758, places=3)
        self.assertEqual(r["N_max_voltage"], 28)
        self.assertTrue(r["String_Voc_cold_V"] <= 1500)
        self.assertTrue(all(r["checks"].values()))


if __name__ == "__main__":
    unittest.main()
