#!/usr/bin/env python3
"""Build frozen ZenFox Setup binaries via PyInstaller — stdlib only (plus pyinstaller).

Run on the TARGET OS (PyInstaller cannot cross-compile):
  Windows:  py -3.12 -m pip install pyinstaller
            py -3.12 tools/build_installer.py --windowed   -> dist/ZenFox-Setup-Windows.exe
  Linux:    python3 tools/build_installer.py               -> dist/ZenFox-Setup-Linux
  macOS:    python3 tools/build_installer.py               -> dist/ZenFox-Setup-macOS

--windowed: no console window on double-click (Windows/macOS GUI use).
            Omit it for a console build that shows --help/log output.
"""
import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_FILES = ["user.js", "LiteFox.js", "Softfox.js", "policies.json",
              "README.md", "LICENSE", "CHANGELOG.md", "VERSION"]
DATA_DIRS = ["vendor/advancedfox"]  # offline AdvancedFox (kept as a tree)
# NOTE: tkinter is deliberately NOT embedded (--exclude-module tkinter):
# the Qt UI (PySide6) is the default and pip-installable everywhere, while the
# tkinter fallback stays source-only for one release. PyInstaller picks up
# PySide6 automatically via its hooks; --hidden-import is belt-and-braces.


def build(windowed=False, name=None, extra_args=()):
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        sys.exit("PyInstaller not found. Install with: pip install pyinstaller")
    for f in ["setup.py", *DATA_FILES]:
        if not (REPO / f).is_file():
            sys.exit(f"Missing expected file: {f} (run from repo root)")

    system = platform.system()
    default_name = {"Windows": "ZenFox-Setup-Windows",
                    "Darwin": "ZenFox-Setup-macOS"}.get(system, "ZenFox-Setup-Linux")
    cmd = [sys.executable, "-m", "PyInstaller",
           "--noconfirm", "--clean", "--onefile",
           "--name", name or default_name,
           "--exclude-module", "tkinter",
           "--hidden-import", "PySide6"]
    sep = ";" if system == "Windows" else ":"
    for f in DATA_FILES:
        cmd += ["--add-data", f"{f}{sep}."]
    for d in DATA_DIRS:
        cmd += ["--add-data", f"{d}{sep}{d}"]
    if windowed:
        cmd.append("--windowed")
    cmd += ["setup.py", *extra_args]
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=REPO, check=True)
    out = REPO / "dist" / ((name or default_name) + (".exe" if system == "Windows" else ""))
    print(f"Built: {out} ({out.stat().st_size // 1024 // 1024} MB)" if out.exists()
          else "PyInstaller finished; check dist/ for output.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Freeze ZenFox Setup with PyInstaller.")
    ap.add_argument("--windowed", action="store_true",
                    help="No console window (double-click GUI on Windows/macOS).")
    ap.add_argument("--name", help="Output binary name (default per-OS).")
    args = ap.parse_args()
    if args.windowed and platform.system() == "Linux":
        print("Note: --windowed has no effect on Linux; building console binary.")
    os.chdir(REPO)
    build(windowed=args.windowed, name=args.name)
