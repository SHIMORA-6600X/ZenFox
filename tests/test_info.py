"""RED tests for info.py — preset metadata + dry-run diff."""
import unittest


class TestInfo(unittest.TestCase):
    def test_presets_known(self):
        from src.zenfox_install import info
        self.assertIn("zenfox", info.PRESETS)
        self.assertIn("advancedfox", info.PRESETS)
        for key in ("name", "version", "source", "best_for", "risk", "files"):
            self.assertIn(key, info.PRESETS["zenfox"])

    def test_compare_table_mentions_both(self):
        from src.zenfox_install import info
        table = info.compare_table()
        self.assertIn("ZenFox", table)
        self.assertIn("AdvancedFox", table)

    def test_parse_user_prefs(self):
        from src.zenfox_install import info
        text = 'user_pref("a.b", true);\n//user_pref("c.d", 1);\nuser_pref("e.f", "x");\n'
        d = info.parse_user_prefs(text)
        self.assertEqual(d, {"a.b": "true", "e.f": '"x"'})

    def test_diff_keys(self):
        from src.zenfox_install import info
        diff = info.diff_keys({"a": 1, "b": 2}, {"b": 2, "c": 3})
        self.assertEqual(diff["only_first"], ["a"])
        self.assertEqual(diff["only_second"], ["c"])
        self.assertEqual(diff["both"], ["b"])


if __name__ == "__main__":
    unittest.main()
