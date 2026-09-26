#!/usr/bin/env python3
"""ZenFox setup entry — stdlib only. Usage: python3 setup.py [flags] (see --help)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.zenfox_install.cli import main


def _venv_python(repo):
    """Interpreter path inside ./.qt-venv (may not exist yet)."""
    import os
    d = "Scripts" if os.name == "nt" else "bin"
    exe = "python.exe" if os.name == "nt" else "python"
    return repo / ".qt-venv" / d / exe


def _venv_marker(repo):
    return repo / ".qt-venv" / ".zenfox-qt-ready"


def _venv_has_qt(venv_py):
    """True when the venv interpreter imports PySide6 (subprocess, no import)."""
    import subprocess
    try:
        subprocess.run([str(venv_py), "-c", "import PySide6"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        return False
    return True


def _ensure_venv_marker(repo):
    """One-time migration: a working .qt-venv without marker gets marked."""
    marker = _venv_marker(repo)
    if marker.is_file():
        return True
    venv_py = _venv_python(repo)
    if not venv_py.is_file() or not _venv_has_qt(venv_py):
        return False
    try:
        marker.touch()
    except OSError:
        return False
    return True


def _reexec_venv(venv_py, initial_tab):
    """Re-exec setup.py under the venv interpreter (never returns)."""
    import os
    flag = "--gui=custom" if initial_tab == "custom" else "--gui"
    child = [str(venv_py), str(Path(__file__).resolve()), flag, *sys.argv[1:]]
    os.execve(str(venv_py), child, {**os.environ, "ZENFOX_QT_BOOTSTRAPPED": "1"})


def _bootstrap_qt(initial_tab):
    """Create ./.qt-venv with PySide6 and re-exec (one-time download).

    Last resort for source-tree runs with no GUI backend at all (no Qt,
    broken tkinter). Frozen builds never reach here (sys._MEIPASS guard);
    the ZENFOX_QT_BOOTSTRAPPED guard prevents re-exec loops on offline
    machines. Returns False when bootstrap is impossible/failed.
    """
    import os
    import subprocess
    if getattr(sys, "_MEIPASS", None):
        return False
    if os.environ.get("ZENFOX_QT_BOOTSTRAPPED"):
        return False  # re-exec already tried: genuinely unavailable/offline
    repo = Path(__file__).resolve().parent
    venv_py = _venv_python(repo)
    if not venv_py.is_file():
        sys.stderr.write("NOTE: no GUI backend — creating .qt-venv with PySide6 "
                         "(one-time download, needs internet)...\n")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(repo / ".qt-venv")],
                           check=True)
        except Exception as e:
            sys.stderr.write(f"NOTE: Qt bootstrap failed ({e}); see error below.\n")
            return False
    if not _venv_has_qt(venv_py):
        sys.stderr.write("NOTE: installing PySide6 into .qt-venv...\n")
        try:
            subprocess.run([str(venv_py), "-m", "pip", "install", "-q", "PySide6>=6.8"],
                           check=True)
        except Exception as e:
            sys.stderr.write(f"NOTE: Qt bootstrap failed ({e}); see error below.\n")
            return False
        if not _venv_has_qt(venv_py):
            return False
    try:
        _venv_marker(repo).touch()
    except OSError:
        pass
    _reexec_venv(venv_py, initial_tab)
    return False


def _launch_gui(initial_tab):
    """Qt-first GUI with tkinter fallback (fallback removed next release).

    Order: system PySide6 → verified .qt-venv (new UI wins over tkinter) →
    tkinter fallback → one-time .qt-venv bootstrap (needs internet once) →
    actionable error. Frozen builds skip bootstrap.
    """
    import os
    repo = Path(__file__).resolve().parent
    try:
        from src.zenfox_install import gui_qt
    except ImportError:
        gui_qt = None
    if gui_qt is not None and gui_qt.available():
        gui_qt.main(initial_tab=initial_tab)
        return
    # New Qt UI wins over the tkinter fallback (loop-guarded: the re-exec
    # child carries ZENFOX_QT_BOOTSTRAPPED and never comes back here).
    if (os.environ.get("ZENFOX_QT_BOOTSTRAPPED") is None
            and _ensure_venv_marker(repo)):
        _reexec_venv(_venv_python(repo), initial_tab)
    try:
        from src.zenfox_install.gui import main as tk_main
    except ImportError:
        tk_main = None
    if tk_main is not None:
        sys.stderr.write("NOTE: PySide6 missing — tkinter fallback "
                         "(pip install PySide6 for the Qt UI).\n")
        try:
            tk_main(initial_tab=initial_tab)
            return
        except ImportError:
            pass  # broken tkinter: fall through to Qt bootstrap
    _bootstrap_qt(initial_tab)  # re-execs into .qt-venv on success
    sys.exit("ERROR: no GUI backend available and Qt bootstrap failed.\n"
             "Install Qt with:  pip install PySide6\n"
             "Or use the CLI:  python3 setup.py --help")


def _default_to_gui():
    """Bare launch (no flags) opens the window instead of the picker.

    Frozen double-click, or source run with dead stdin (where the
    interactive picker could never work anyway — it died with EOFError).
    Terminal users with a live stdin keep the classic picker.
    """
    if len(sys.argv) != 1:
        return False
    if getattr(sys, "_MEIPASS", None) is not None:
        return True
    return not sys.stdin.isatty()


def _run_cli():
    """CLI entry with a clean Ctrl+C path (exit 130, no traceback)."""
    try:
        return main()
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    _gui_arg = next((a for a in sys.argv
                     if a == "--gui" or a.startswith("--gui=")), None)
    if _gui_arg is None:
        if _default_to_gui():
            _launch_gui(initial_tab="simple")
        else:
            raise SystemExit(_run_cli())
    else:
        sys.argv.remove(_gui_arg)
        _launch_gui(initial_tab="custom" if _gui_arg == "--gui=custom" else "simple")
