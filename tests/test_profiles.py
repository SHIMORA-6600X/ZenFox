"""RED tests for profiles.py — Firefox profile discovery on Win/Linux/macOS.

Run: python3 -m unittest tests.test_profiles -v
"""
import configparser
import os
import tempfile
import unittest
from pathlib import Path


def _write_ini(path: Path, sections: dict) -> None:
    cp = configparser.ConfigParser()
    for name, kv in sections.items():
        cp[name] = kv
    with open(path, "w") as f:
        cp.write(f)


class TestDataRoots(unittest.TestCase):
    def test_linux_roots_include_variants(self):
        from src.zenfox_install import profiles
        roots = profiles.data_roots(os_override="linux", home_override="/home/u")
        s = [r.as_posix() for r in roots]  # portable: forward slashes everywhere
        self.assertIn("/home/u/.mozilla/firefox", s)
        self.assertTrue(any("org.mozilla.firefox" in r for r in s), "flatpak missing")
        self.assertTrue(any("snap/firefox" in r for r in s), "snap missing")

    def test_windows_roots_use_appdata(self):
        from src.zenfox_install import profiles
        env = {"APPDATA": "C:/Users/u/AppData/Roaming"}
        roots = profiles.data_roots(os_override="windows", env_override=env)
        self.assertTrue(any("Mozilla" in str(r) and "Firefox" in str(r) for r in roots))

    def test_macos_roots(self):
        from src.zenfox_install import profiles
        roots = profiles.data_roots(os_override="macos", home_override="/Users/u")
        self.assertTrue(any("Application Support" in str(r) for r in roots))


class TestParseIni(unittest.TestCase):
    def test_parses_relative_and_default(self):
        from src.zenfox_install import profiles
        with tempfile.TemporaryDirectory() as d:
            ini = Path(d) / "profiles.ini"
            _write_ini(ini, {
                "Profile0": {"Name": "default", "Path": "abcd.default", "IsRelative": "1", "Default": "1"},
                "Profile1": {"Name": "work", "Path": "/data/work-profile", "IsRelative": "0"},
            })
            out = profiles.parse_profiles_ini(ini)
            self.assertEqual(len(out), 2)
            by_name = {p["name"]: p for p in out}
            self.assertEqual(by_name["default"]["path"], Path(d) / "abcd.default")
            self.assertTrue(by_name["default"]["is_default"])
            self.assertEqual(by_name["work"]["path"], Path("/data/work-profile"))
            self.assertFalse(by_name["work"]["is_default"])

    def test_missing_file_returns_empty(self):
        from src.zenfox_install import profiles
        self.assertEqual(profiles.parse_profiles_ini(Path("/nope/profiles.ini")), [])

    def test_ignores_non_profile_sections(self):
        from src.zenfox_install import profiles
        with tempfile.TemporaryDirectory() as d:
            ini = Path(d) / "profiles.ini"
            _write_ini(ini, {
                "General": {"StartWithLastProfile": "1"},
                "Profile0": {"Name": "a", "Path": "aaa", "IsRelative": "1"},
            })
            out = profiles.parse_profiles_ini(ini)
            self.assertEqual(len(out), 1)
            self.assertEqual(out[0]["name"], "a")


class TestResolve(unittest.TestCase):
    def test_resolve_by_name_and_path(self):
        from src.zenfox_install import profiles
        with tempfile.TemporaryDirectory() as d:
            listed = Path(d) / "aaa"
            listed.mkdir()
            unlisted = Path(d) / "bbb"
            unlisted.mkdir()
            fake = [
                {"name": "default", "path": listed, "is_default": True},
            ]
            self.assertEqual(profiles.resolve_profile("default", fake), listed)
            self.assertEqual(profiles.resolve_profile(str(listed), fake), listed)
            # existing dir need not be listed
            self.assertEqual(profiles.resolve_profile(str(unlisted), fake), unlisted)

    def test_resolve_unknown_raises(self):
        from src.zenfox_install import profiles
        with self.assertRaises(profiles.ProfileNotFoundError):
            profiles.resolve_profile("nope", [])


class TestCreateProfile(unittest.TestCase):
    def test_creates_dir_and_ini_from_scratch(self):
        from src.zenfox_install import profiles
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "firefox"
            got = profiles.create_profile(root, name="zenfox")
            self.assertTrue(got["path"].is_dir())
            self.assertTrue((root / "profiles.ini").is_file())
            self.assertTrue(got["is_default"])  # first profile becomes default
            found = profiles.parse_profiles_ini(root / "profiles.ini")
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0]["path"], got["path"])
            self.assertEqual(found[0]["name"], "zenfox")

    def test_second_profile_does_not_steal_default(self):
        from src.zenfox_install import profiles
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "firefox"
            first = profiles.create_profile(root, name="zenfox")
            second = profiles.create_profile(root, name="work")
            self.assertFalse(second["is_default"])
            found = {p["name"]: p for p in profiles.parse_profiles_ini(root / "profiles.ini")}
            self.assertTrue(found["zenfox"]["is_default"])
            self.assertFalse(found["work"]["is_default"])
            self.assertNotEqual(first["path"], second["path"])

    def test_preserves_key_case_and_other_sections(self):
        from src.zenfox_install import profiles
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "firefox"
            root.mkdir()
            (root / "profiles.ini").write_text(
                "[General]\nStartWithLastProfile=1\nVersion=2\n\n"
                "[Profile0]\nName=old\nPath=old.one\nIsRelative=1\nDefault=1\n")
            profiles.create_profile(root, name="new")
            import configparser
            cp = configparser.ConfigParser()
            cp.optionxform = str
            cp.read(root / "profiles.ini", encoding="utf-8")
            self.assertEqual(cp["General"]["StartWithLastProfile"], "1")
            self.assertEqual(cp["Profile0"]["Name"], "old")  # case + values kept
            self.assertEqual(cp["Profile1"]["Name"], "new")

    def test_choose_creation_root_prefers_existing(self):
        from src.zenfox_install import profiles
        with tempfile.TemporaryDirectory() as d:
            missing = Path(d) / "nope"
            existing = Path(d) / "yes"
            existing.mkdir()
            self.assertEqual(profiles.choose_creation_root([missing, existing]), existing)
            self.assertEqual(profiles.choose_creation_root([missing]), missing)


if __name__ == "__main__":
    unittest.main()
