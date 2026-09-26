"""Admin policies.json handling — stdlib only.

policies.json does NOT go in the profile; it goes in Firefox's distribution/
dir which needs admin rights. Non-admin users get profile-only install.
"""
import os
import shutil
from pathlib import Path


def is_admin():
    try:
        if os.name == "nt":
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        return os.geteuid() == 0
    except Exception:
        return False


def distribution_dirs(os_name, firefox_dir=None):
    os_name = os_name.lower()
    if os_name == "windows":
        base = Path(firefox_dir) if firefox_dir else Path(r"C:\Program Files\Mozilla Firefox")
        return [base / "distribution"]
    if os_name == "macos":
        base = Path(firefox_dir) if firefox_dir else Path("/Applications/Firefox.app/Contents/Resources")
        return [base / "distribution"]
    candidates = [
        Path("/usr/lib/firefox/distribution"),
        Path("/usr/lib64/firefox/distribution"),
        Path("/etc/firefox/policies"),
    ]
    if firefox_dir:
        candidates.insert(0, Path(firefox_dir) / "distribution")
    return candidates


def install_policies(src_file, dest_dir):
    src_file, dest_dir = Path(src_file), Path(dest_dir)
    if not src_file.is_file():
        raise ValueError(f"policies source missing: {src_file}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "policies.json"
    shutil.copy2(src_file, dest)
    return dest
