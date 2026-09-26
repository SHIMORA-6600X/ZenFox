"""Tests for gui.py pure helpers — headless-safe (no tkinter import)."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock


class TestGuiHelpers(unittest.TestCase):
    def test_describe_preset(self):
        from src.zenfox_install import gui
        card = gui.describe_preset("zenfox")
        self.assertIn("ZenFox", card)
        self.assertIn("Risk", card)
        card2 = gui.describe_preset("advancedfox")
        self.assertIn("AdvancedFox", card2)

    def test_files_for_preset(self):
        from src.zenfox_install import gui
        self.assertEqual(gui.files_for_preset("zenfox"), ["user.js"])
        self.assertEqual(gui.files_for_preset("zenfox", True, True),
                         ["user.js", "LiteFox.js", "Softfox.js"])
        self.assertEqual(gui.files_for_preset("advancedfox", True, True), ["user.js"])

    def test_validate_inputs(self):
        from src.zenfox_install import gui, info
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(gui.validate_inputs("zenfox", d), [])
            self.assertTrue(gui.validate_inputs("zenfox", "/nope"))
            self.assertTrue(gui.validate_inputs("bogus", d))
            # vendored default (empty or release page) needs no URL/hash
            self.assertEqual(gui.validate_inputs("advancedfox", d), [])
            self.assertEqual(gui.validate_inputs("advancedfox", d, info.ADV_DEFAULT_URL), [])
            # custom URL: must be hash-pinned .zip
            self.assertTrue(gui.validate_inputs("advancedfox", d,
                                                "https://x/releases", ""))
            self.assertTrue(gui.validate_inputs("advancedfox", d,
                                                "https://x/a.zip", ""))
            self.assertEqual(gui.validate_inputs("advancedfox", d,
                                                 "https://x/a.zip", "ab" * 32), [])

    def test_module_import_needs_no_tkinter(self):
        import sys
        self.assertNotIn("tkinter", sys.modules)
        import src.zenfox_install.gui  # noqa — must not import tkinter at top
        self.assertNotIn("tkinter", sys.modules)

    def test_theme_complete_and_stub_safe(self):
        from unittest.mock import MagicMock
        from src.zenfox_install import gui
        for key in ("bg", "surface", "card", "entry", "fg", "muted",
                    "accent", "accent_fg", "border", "select"):
            self.assertIn(key, gui.THEME)
            self.assertTrue(gui.THEME[key].startswith("#"))
        # must not raise with stub modules (proves no real tk calls at import)
        gui.apply_theme(MagicMock(), MagicMock(), MagicMock())

    def test_bundled_tk_runtime_present(self):
        import platform
        import pathlib
        base = pathlib.Path(__file__).resolve().parent.parent / "thirdparty" / "tk" / "linux-x86_64"
        for name in ("libtk8.6.so", "libtcl8.6.so"):
            self.assertTrue((base / name).is_file(), f"missing {name}")
        for name in ("tcl8.6", "tk8.6"):
            self.assertTrue((base / name).is_dir(), f"missing dir {name}")
        if platform.system() == "Linux" and platform.machine() == "x86_64":
            import ctypes
            # loadable by this interpreter (proves ABI match, no import needed)
            ctypes.CDLL(str(base / "libtcl8.6.so"))
            ctypes.CDLL(str(base / "libtk8.6.so"))


class TestSmoothScroller(unittest.TestCase):
    def _pump(self, box):
        while box:
            box.pop(0)()

    def test_single_notch_glides_and_drains(self):
        from src.zenfox_install.gui import SmoothScroller
        calls, box = [], []
        w = MagicMock()
        w.yview_scroll.side_effect = lambda s, u: calls.append(s)
        sc = SmoothScroller(w, lambda ms, fn: box.append(fn))
        sc.scroll(1)
        self._pump(box)
        self.assertEqual(sum(calls), 104)
        self.assertGreater(len(calls), 3, "must glide in steps, not one jump")
        steps = [abs(c) for c in calls]
        self.assertLessEqual(max(steps), 37)
        self.assertEqual(steps, sorted(steps, reverse=True), "ease-out: decreasing")

    def test_opposite_notches_cancel(self):
        from src.zenfox_install.gui import SmoothScroller
        calls, box = [], []
        w = MagicMock()
        w.yview_scroll.side_effect = lambda s, u: calls.append(s)
        sc = SmoothScroller(w, lambda ms, fn: box.append(fn))
        sc.scroll(1)
        sc.scroll(-1)
        self._pump(box)
        self.assertEqual(calls, [])

    def test_runaway_capped(self):
        from src.zenfox_install.gui import SmoothScroller
        calls, box = [], []
        w = MagicMock()
        w.yview_scroll.side_effect = lambda s, u: calls.append(s)
        sc = SmoothScroller(w, lambda ms, fn: box.append(fn))
        sc.scroll(100)
        self._pump(box)
        self.assertEqual(sum(calls), 312)

    def test_fractional_notches(self):
        from src.zenfox_install.gui import SmoothScroller
        calls, box = [], []
        w = MagicMock()
        w.yview_scroll.side_effect = lambda s, u: calls.append(s)
        sc = SmoothScroller(w, lambda ms, fn: box.append(fn))
        sc.scroll(0.5)
        self._pump(box)
        self.assertEqual(sum(calls), 52)


if __name__ == "__main__":
    unittest.main()
