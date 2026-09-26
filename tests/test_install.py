"""RED tests for install.py + policies.py."""
import tempfile
import unittest
from pathlib import Path


class TestInstall(unittest.TestCase):
    def _profile(self, d):
        p = Path(d) / "prof"
        p.mkdir()
        (p / "user.js").write_text("old")
        (p / "prefs.js").write_text("prefs")
        return p

    def test_backup_and_revert_roundtrip(self):
        from src.zenfox_install import install
        with tempfile.TemporaryDirectory() as d:
            prof = self._profile(d)
            backup = install.backup_profile(prof)
            self.assertTrue((backup / "user.js").exists())
            self.assertTrue((backup / "manifest.txt").exists())
            (prof / "user.js").write_text("new")
            install.revert_backup(prof, backup)
            self.assertEqual((prof / "user.js").read_text(), "old")

    def test_install_copies_only_allowlisted(self):
        from src.zenfox_install import install
        with tempfile.TemporaryDirectory() as d:
            prof = Path(d) / "prof"
            prof.mkdir()
            src = Path(d) / "src"
            src.mkdir()
            (src / "user.js").write_text("v")
            (src / "evil.js").write_text("evil")
            got = install.install_files(src, prof, files=["user.js"])
            self.assertEqual((prof / "user.js").read_text(), "v")
            self.assertFalse((prof / "evil.js").exists())
            self.assertIn("user.js", got)

    def test_install_refuses_missing_profile(self):
        from src.zenfox_install import install
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(install.InstallError):
                install.install_files(Path(d) / "src", Path(d) / "noprof", files=["user.js"])

    def test_firefox_running_detected(self):
        from src.zenfox_install import install
        with tempfile.TemporaryDirectory() as d:
            prof = Path(d) / "prof"
            prof.mkdir()
            self.assertFalse(install.firefox_lock_present(prof))
            (prof / "lock").write_text("")
            self.assertTrue(install.firefox_lock_present(prof))


class TestPolicies(unittest.TestCase):
    def test_distribution_dirs_per_os(self):
        from src.zenfox_install import policies
        self.assertTrue(any("Firefox" in str(p) for p in policies.distribution_dirs("windows")))
        self.assertTrue(any("distribution" in str(p) for p in policies.distribution_dirs("linux")))
        self.assertTrue(any("Firefox.app" in str(p) for p in policies.distribution_dirs("macos")))

    def test_install_policies_copies(self):
        from src.zenfox_install import policies
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "policies.json"
            src.write_text("{}")
            dest_dir = Path(d) / "dist"
            dest = policies.install_policies(src, dest_dir)
            self.assertTrue(dest.exists())


if __name__ == "__main__":
    unittest.main()
