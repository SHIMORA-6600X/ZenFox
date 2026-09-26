"""RED tests for sections.py — per-section parse/generate for Custom mode."""
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class TestParse(unittest.TestCase):
    def test_user_js_section_count_and_titles(self):
        from src.zenfox_install import sections
        preamble, secs = sections.parse_file(REPO / "user.js")
        titles = [s["title"] for s in secs]
        self.assertEqual(len(secs), 9)
        self.assertIn("GENERAL", titles)
        self.assertIn("NETWORK", titles)
        self.assertIn("TAB UNLOAD", titles)
        self.assertEqual(len(set(titles)), len(titles), "duplicate titles")

    def test_litefox_section_count(self):
        from src.zenfox_install import sections
        _, secs = sections.parse_file(REPO / "LiteFox.js")
        self.assertEqual(len(secs), 12)
        pocket = [s for s in secs if s["title"] == "POCKET"][0]
        self.assertEqual(len(pocket["prefs"]), 0)
        self.assertTrue(pocket["empty"])

    def test_active_counts_match_lint_ground_truth(self):
        from src.zenfox_install import sections
        _, u = sections.parse_file(REPO / "user.js")
        _, l = sections.parse_file(REPO / "LiteFox.js")
        self.assertEqual(sum(len(s["prefs"]) for s in u), 63)
        self.assertEqual(sum(len(s["prefs"]) for s in l), 105)

    def test_pref_keys_and_comments_captured(self):
        from src.zenfox_install import sections
        _, secs = sections.parse_file(REPO / "user.js")
        net = [s for s in secs if s["title"] == "NETWORK"][0]
        keys = [p["key"] for p in net["prefs"]]
        self.assertIn("network.http.max-connections", keys)


class TestGenerate(unittest.TestCase):
    def test_subset_build_excludes_disabled(self):
        from src.zenfox_install import sections
        preamble, secs = sections.parse_file(REPO / "user.js")
        out = sections.build_custom_user_js(preamble, secs, {"NETWORK", "TAB UNLOAD"})
        self.assertIn("SECTION: NETWORK", out)
        self.assertIn("SECTION: TAB UNLOAD", out)
        self.assertNotIn("SECTION: MEDIA CACHE", out)
        self.assertIn("Custom build", out)

    def test_every_single_section_build_parses(self):
        """Regression: no section may leak the next banner (unclosed comment)."""
        import os
        import tempfile
        from src.zenfox_install import sections
        try:
            subprocess.run(["node", "--version"], capture_output=True, timeout=10)
        except FileNotFoundError:
            self.skipTest("node not installed")
        for fname in ("user.js", "LiteFox.js"):
            preamble, secs = sections.parse_file(REPO / fname)
            for s in secs:
                if s["empty"]:
                    continue
                out = sections.build_custom_user_js(preamble, secs, {s["title"]})
                with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                                  encoding="utf-8") as f:
                    f.write(out)
                    tmp = f.name
                try:
                    r = subprocess.run(["node", "--check", tmp],
                                       capture_output=True, text=True, timeout=30)
                finally:
                    os.unlink(tmp)
                self.assertEqual(r.returncode, 0, f"{fname}:{s['title']}: {r.stderr}")

    def test_generated_file_parses_as_js(self):
        from src.zenfox_install import sections
        import tempfile
        import os
        preamble, secs = sections.parse_file(REPO / "user.js")
        out = sections.build_custom_user_js(preamble, secs,
                                            {s["title"] for s in secs})
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                           encoding="utf-8") as f:
            f.write(out)
            tmp = f.name
        try:
            r = subprocess.run(["node", "--check", tmp],
                               capture_output=True, text=True, timeout=30)
        except FileNotFoundError:
            self.skipTest("node not installed")
        finally:
            os.unlink(tmp)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_summarize_and_count(self):
        from src.zenfox_install import sections
        _, secs = sections.parse_file(REPO / "user.js")
        net = [s for s in secs if s["title"] == "NETWORK"][0]
        line = sections.summarize(net, enabled=False)
        self.assertIn("OFF", line)
        self.assertIn("NETWORK", line)
        n = sections.count_active(secs, {"NETWORK"})
        self.assertEqual(n, len(net["prefs"]))


if __name__ == "__main__":
    unittest.main()
