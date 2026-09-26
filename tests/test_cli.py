"""Tests for cli.py — parser contract (additive flags only)."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parent.parent


class TestCli(unittest.TestCase):
    def test_parser_defaults(self):
        from src.zenfox_install import cli
        args = cli.build_parser().parse_args([])
        self.assertIsNone(args.preset)
        self.assertFalse(args.with_lite)
        self.assertFalse(args.dry_run)
        self.assertEqual(args.zen_tag, "v157")
        self.assertEqual(args.adv_level, "medium")
        self.assertIsNone(args.sections)

    def test_parser_preset_choices(self):
        from src.zenfox_install import cli
        args = cli.build_parser().parse_args(["--preset", "zenfox", "--profile", "x"])
        self.assertEqual(args.preset, "zenfox")

    def test_compare_table_stable(self):
        from src.zenfox_install import info
        t = info.compare_table()
        self.assertIn("ZenFox", t)
        self.assertIn("AdvancedFox", t)

    def test_adv_resolves_vendored_offline(self):
        from src.zenfox_install import cli
        args = cli.build_parser().parse_args(["--preset", "advancedfox"])
        with tempfile.TemporaryDirectory() as tmp:
            src, files = cli.resolve_adv_files(args, tmp)
            content = (Path(src) / "user.js").read_text()
            self.assertIn("user_pref", content)
            self.assertIn("AdvancedFox", content)

    def test_adv_levels_differ(self):
        from src.zenfox_install import cli
        weak = cli.build_parser().parse_args(["--adv-level", "weak"])
        strong = cli.build_parser().parse_args(["--adv-level", "strong"])
        with tempfile.TemporaryDirectory() as tmp:
            w, _ = cli.resolve_adv_files(weak, tmp + "/w")
            s, _ = cli.resolve_adv_files(strong, tmp + "/s")
            self.assertNotEqual((w / "user.js").read_text(), (s / "user.js").read_text())

    def test_adv_custom_url_requires_zip_and_sha(self):
        from src.zenfox_install import cli, sources
        args = cli.build_parser().parse_args(
            ["--preset", "advancedfox", "--adv-url", "https://x/page"])
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(sources.SourceError):
                cli.resolve_adv_files(args, tmp)

    def test_custom_build_subset_and_unknown(self):
        from src.zenfox_install import cli, sources
        files = cli.build_custom_files(REPO, "NETWORK,TAB UNLOAD")
        self.assertIn("SECTION: NETWORK", files["user.js"])
        self.assertNotIn("SECTION: MEDIA CACHE", files["user.js"])
        with self.assertRaises(sources.SourceError):
            cli.build_custom_files(REPO, "NOPE")
        lite = cli.build_custom_files(REPO, None, "URL BAR")
        self.assertIn("SECTION: URL BAR", lite["LiteFox.js"])
        self.assertNotIn("SECTION: POCKET", lite["LiteFox.js"])

    def test_eof_on_stdin_aborts_cleanly_not_traceback(self):
        """Double-clicked binary with dead stdin: return 1, never raise."""
        from src.zenfox_install import cli
        with patch.object(cli, "_is_tty", return_value=True), \
             patch("builtins.input", side_effect=EOFError):
            self.assertEqual(cli.main([]), 1)

    def test_eof_in_profile_picker_aborts_cleanly(self):
        from src.zenfox_install import cli
        with patch("builtins.input", side_effect=EOFError):
            self.assertIsNone(cli.pick_profile([]))

    def test_eof_in_preset_picker_aborts_cleanly(self):
        from src.zenfox_install import cli
        with patch("builtins.input", side_effect=EOFError):
            self.assertIsNone(cli.pick_preset())


if __name__ == "__main__":
    unittest.main()
