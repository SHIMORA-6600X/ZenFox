"""Qt GUI tests: drive the REAL gui_qt.MainWindow offscreen (no X server).

Requires PySide6; skips cleanly without it (fallback-tkinter installs).
Run: QT_QPA_PLATFORM=offscreen python3 -m unittest tests.test_gui_qt -v
"""
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

REPO = Path(__file__).resolve().parent.parent
HAS_QT = importlib.util.find_spec("PySide6") is not None


@unittest.skipUnless(HAS_QT, "PySide6 not installed")
class TestQtWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PySide6.QtWidgets import QApplication
        cls._app = QApplication.instance() or QApplication([])

    def _window(self, **kw):
        from src.zenfox_install import gui_qt
        return gui_qt.MainWindow(**kw)

    def test_simple_tab_is_default_and_custom_selectable(self):
        w = self._window()
        self.assertEqual(w.tabs.tabText(0), "Simple")
        self.assertEqual(w.tabs.tabText(1), "Custom")
        self.assertEqual(w.tabs.currentIndex(), 0)
        w2 = self._window(initial_tab="custom")
        self.assertEqual(w2.tabs.currentIndex(), 1)

    def test_preset_info_card_matches_helper(self):
        from src.zenfox_install.gui import describe_preset
        w = self._window()
        self.assertIn("ZenFox", w.info_box.toPlainText())
        w.preset_zen.setChecked(False)
        w.preset_adv.setChecked(True)
        self.assertEqual(w.info_box.toPlainText(), describe_preset("advancedfox"))

    def test_custom_tab_loads_21_section_rows(self):
        w = self._window(initial_tab="custom")
        w.load_custom()
        rows = w.section_list.count()
        self.assertEqual(rows, 21)
        # one upstream-removed (empty) section starts OFF: 20/21
        self.assertIn("20/21", w.count_label.text())

    def test_toggle_off_appends_changelog_and_updates_count(self):
        w = self._window(initial_tab="custom")
        w.load_custom()
        before = w.count_label.text()
        self.assertIn("20/21", before)
        first = w.section_list.item(0)
        first.setCheckState(__import__("PySide6.QtCore", fromlist=["Qt"]).Qt.Unchecked)
        log = w.changelog_box.toPlainText()
        self.assertIn("OFF", log)
        self.assertIn("19/21", w.count_label.text())

    def test_detail_preview_shows_section_prefs(self):
        w = self._window(initial_tab="custom")
        w.load_custom()
        title = w.custom_state["user"][0]["title"]
        w.show_detail(title)
        body = w.detail_box.toPlainText()
        self.assertIn(title, body)
        first_key = w.custom_state["user"][0]["prefs"][0]["key"]
        self.assertIn(first_key, body)

    def test_apply_custom_installs_only_enabled_sections(self):
        from src.zenfox_install import gui_qt
        w = self._window(initial_tab="custom")
        w.load_custom()
        with tempfile.TemporaryDirectory() as prof:
            dropped = w.custom_state["user"][0]["title"]
            w.custom_state["enabled_user"][dropped] = False
            msgs = []
            gui_qt.do_apply_custom(
                msgs.append, Path(prof),
                dict(w.custom_state["enabled_user"]),
                None,
                w.custom_state["user"], w.custom_state["lite"])
            installed = (Path(prof) / "user.js").read_text()
            from src.zenfox_install import sections as _s
            active = _s.count_active(w.custom_state["user"],
                                     {t for t, v in w.custom_state["enabled_user"].items() if v})
            self.assertTrue((Path(prof) / "user.js").is_file())
            self.assertTrue(any("Custom installed" in m for m in msgs))
            # dropped section's prefs are absent from the installed file
            dropped_keys = {p["key"] for p in w.custom_state["user"][0]["prefs"]}
            installed_keys = {l.split('"')[1] for l in installed.splitlines()
                              if l.startswith("user_pref(")}
            self.assertTrue(dropped_keys.isdisjoint(installed_keys))
            self.assertGreater(active, 0)

    def test_simple_install_roundtrip_on_fake_profile(self):
        from src.zenfox_install import gui_qt
        with tempfile.TemporaryDirectory() as prof:
            (Path(prof) / "user.js").write_text("old")
            (Path(prof) / "prefs.js").write_text("old")
            msgs = []
            gui_qt.do_install(msgs.append, "zenfox", Path(prof),
                              with_lite=True, with_soft=False,
                              with_policies=False, adv_level="medium")
            self.assertTrue((Path(prof) / "LiteFox.js").is_file())
            self.assertTrue(any("Installed into" in m for m in msgs))
            backups = sorted(Path(prof).glob("zenfox-backup-*"))
            self.assertTrue(backups)
            gui_qt.do_revert(msgs.append, Path(prof))
            self.assertEqual((Path(prof) / "user.js").read_text(), "old")

    def test_invalid_profile_reports_error_not_crash(self):
        from src.zenfox_install import gui_qt
        msgs = []
        gui_qt.do_install(msgs.append, "zenfox", Path("/nonexistent-profile-xyz"),
                          with_lite=False, with_soft=False,
                          with_policies=False, adv_level="medium")
        self.assertTrue(any("ERROR" in m for m in msgs))

    def test_qt_backend_reports_available(self):
        from src.zenfox_install import gui_qt
        self.assertTrue(gui_qt.available())
        gui_qt.need_qt()  # must not raise when PySide6 imports

    def test_threaded_run_installs_and_logs(self):
        import time
        from PySide6.QtWidgets import QApplication
        w = self._window()
        with tempfile.TemporaryDirectory() as prof:
            (Path(prof) / "prefs.js").write_text("old")
            w.profile_combo.setCurrentText(prof)
            w.run("install")  # no confirm dialog when confirm=False
            deadline = time.time() + 10
            while w._threads and time.time() < deadline:
                QApplication.processEvents()
                time.sleep(0.05)
            self.assertFalse(w._threads, "worker thread did not finish")
            QApplication.processEvents()
            self.assertTrue((Path(prof) / "user.js").is_file())
            self.assertIn("Installed into", w.log_box.toPlainText())


if __name__ == "__main__":
    unittest.main()
