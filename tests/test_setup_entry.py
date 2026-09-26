"""Tests for setup.py entry logic (Qt bootstrap + venv selection) — stdlib only."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class TestQtBootstrapGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        repo = __import__("pathlib").Path(__file__).resolve().parent.parent
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        global setup_mod
        import setup as setup_mod

    def test_second_attempt_refuses_without_side_effects(self):
        os.environ["ZENFOX_QT_BOOTSTRAPPED"] = "1"
        try:
            self.assertFalse(setup_mod._bootstrap_qt("simple"))
        finally:
            del os.environ["ZENFOX_QT_BOOTSTRAPPED"]

    def test_frozen_build_never_bootstraps(self):
        sys._MEIPASS = "/fake/frozen"  # noqa: SLF001 (test-only simulation)
        try:
            self.assertFalse(setup_mod._bootstrap_qt("custom"))
        finally:
            del sys._MEIPASS


class TestVenvSelection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        repo = Path(__file__).resolve().parent.parent
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        global setup_mod
        import setup as setup_mod

    def test_marker_short_circuits_without_subprocess(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".qt-venv" / "bin").mkdir(parents=True)
            (repo / ".qt-venv" / "bin" / "python").touch()
            (repo / ".qt-venv" / ".zenfox-qt-ready").touch()
            with patch("subprocess.run") as run:
                self.assertTrue(setup_mod._ensure_venv_marker(repo))
                run.assert_not_called()

    def test_missing_venv_is_not_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(setup_mod._ensure_venv_marker(Path(tmp)))

    def test_venv_without_qt_is_not_ready(self):
        # broken interpreter (or missing file) is never "ready" — no Qt needed
        with patch("subprocess.run", side_effect=FileNotFoundError("nope")):
            self.assertFalse(setup_mod._venv_has_qt(Path("/nonexistent/python")))
        self.assertFalse(setup_mod._venv_has_qt(Path("/nonexistent/python")))
        self.assertFalse(setup_mod._ensure_venv_marker(Path("/nonexistent-repo")))

    @unittest.skipUnless(__import__("importlib").util.find_spec("PySide6") is not None,
                         "needs an interpreter with PySide6")
    def test_venv_with_qt_gets_marked(self):
        # hardlink THIS interpreter (proven to import PySide6) into a fake
        # venv layout — instant, portable (NTFS supports hardlinks), no venv
        # needed since _venv_has_qt only runs `<link> -c "import PySide6"`.
        import os as _os
        import shutil as _shutil
        tmp = tempfile.mkdtemp()
        # Wine/Windows may lock the executed hardlink: strict assertions,
        # forgiving teardown.
        self.addCleanup(lambda: _shutil.rmtree(tmp, ignore_errors=True))
        repo = Path(tmp)
        bindir = repo / ".qt-venv" / ("Scripts" if _os.name == "nt" else "bin")
        bindir.mkdir(parents=True)
        link = bindir / ("python.exe" if _os.name == "nt" else "python")
        try:
            _os.link(sys.executable, link)
        except OSError:
            self.skipTest("cannot hardlink interpreter")
        self.assertTrue(setup_mod._venv_has_qt(link))
        self.assertTrue(setup_mod._ensure_venv_marker(repo))
        self.assertTrue((repo / ".qt-venv" / ".zenfox-qt-ready").is_file())

    def test_reexec_uses_venv_and_loop_guard(self):
        with patch("os.execve") as exe:
            venv_py = setup_mod._venv_python(Path("/x"))
            setup_mod._reexec_venv(venv_py, "custom")
            args = exe.call_args[0]
            self.assertEqual(args[0], str(venv_py))  # platform-correct path
            self.assertIn("--gui=custom", args[1])
            self.assertEqual(args[2].get("ZENFOX_QT_BOOTSTRAPPED"), "1")

    def test_frozen_bare_launch_defaults_to_gui(self):
        setup_mod.sys._MEIPASS = "/fake/bundle"  # noqa: SLF001 (test-only)
        try:
            with patch.object(setup_mod.sys, "argv", ["ZenFox-Setup"]):
                self.assertTrue(setup_mod._default_to_gui())
            with patch.object(setup_mod.sys, "argv", ["ZenFox-Setup", "--help"]):
                self.assertFalse(setup_mod._default_to_gui())
        finally:
            del setup_mod.sys._MEIPASS

    def test_source_piped_stdin_defaults_to_gui(self):
        if getattr(sys, "_MEIPASS", None):
            self.skipTest("frozen-only inverse check")
        with patch.object(setup_mod.sys, "argv", ["setup.py"]), \
             patch.object(setup_mod.sys.stdin, "isatty", return_value=False):
            self.assertTrue(setup_mod._default_to_gui())

    def test_source_tty_stays_interactive_cli(self):
        if getattr(sys, "_MEIPASS", None):
            self.skipTest("frozen-only inverse check")
        with patch.object(setup_mod.sys, "argv", ["setup.py"]), \
             patch.object(setup_mod.sys.stdin, "isatty", return_value=True):
            self.assertFalse(setup_mod._default_to_gui())

    def test_ctrl_c_exits_130_without_traceback(self):
        with patch.object(setup_mod, "main", side_effect=KeyboardInterrupt):
            self.assertEqual(setup_mod._run_cli(), 130)


if __name__ == "__main__":
    unittest.main()
