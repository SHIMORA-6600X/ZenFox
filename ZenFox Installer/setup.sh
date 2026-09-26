#!/usr/bin/env bash
# ZenFox Setup — double-click launcher (no terminal needed).
# With NO args: picks the best UI automatically (offline, nothing to download):
#   1. Qt GUI       (PySide6 — pip-installable, native look, Simple + Custom tabs)
#   2. tkinter GUI  (system tkinter, else bundled thirdparty/tk runtime — fallback this release)
#   3. offer one-click PySide6 install via pip (user-level, no admin)
#   4. offer one-click Tk system install (only if bundled is missing/unusable)
#   5. zenity dialogs (drives setup.py underneath)
#   6. terminal fallback (opens one only as a last resort)
# With args: runs the CLI directly, e.g.
#   ./setup.sh --preset advancedfox --adv-level strong --profile work --yes
#   ./setup.sh --gui   (force the windowed UI)
set -u
cd "$(dirname "$0")"

have() { command -v "$1" >/dev/null 2>&1; }
if ! have python3; then
  echo "ERROR: python3 not found. Install Python 3.8+ then re-run setup.sh." >&2
  exit 2
fi

# Explicit CLI use: forward everything to setup.py, no UI detection.
if [ "$#" -gt 0 ]; then
  exec python3 setup.py "$@"
fi

has_display() { [ -n "${DISPLAY:-}" ] || [ -n "${WAYLAND_DISPLAY:-}" ]; }
qt_ok() { python3 -c "import PySide6" 2>/dev/null; }
tk_ok() { python3 -c "import tkinter" 2>/dev/null; }
gui_ok() { qt_ok || tk_ok; }

# Interpreter for the GUI: verified .qt-venv (new Qt UI) always wins over
# system python (tkinter fallback). One-time migration: a working .qt-venv
# without the marker file gets marked after a real import check.
gui_python() {
  if [ ! -f "$PWD/.qt-venv/.zenfox-qt-ready" ] && [ -x "$PWD/.qt-venv/bin/python" ]; then
    if "$PWD/.qt-venv/bin/python" -c "import PySide6" 2>/dev/null; then
      touch "$PWD/.qt-venv/.zenfox-qt-ready" 2>/dev/null || true
    fi
  fi
  if [ -f "$PWD/.qt-venv/.zenfox-qt-ready" ]; then
    printf '%s' "$PWD/.qt-venv/bin/python"
  else
    printf 'python3'
  fi
}
venv_ready() { [ -f "$PWD/.qt-venv/.zenfox-qt-ready" ]; }

# Bundled Tk runtime (thirdparty/tk): zero-install fallback for Linux x86_64
# machines whose Python lacks tkinter. System tkinter always wins when present.
bundle_tk_dir() {
  [ "$(uname -s)" = "Linux" ] && [ "$(uname -m)" = "x86_64" ] || return 0
  local d="$PWD/thirdparty/tk/linux-x86_64"
  [ -f "$d/libtk8.6.so" ] && [ -d "$d/tk8.6" ] && [ -d "$d/tcl8.6" ] && printf '%s' "$d"
  return 0
}

try_bundle_tk() {
  local d="$(bundle_tk_dir)"
  [ -n "$d" ] || return 1
  export LD_LIBRARY_PATH="$d${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  export TCL_LIBRARY="$d/tcl8.6"
  export TK_LIBRARY="$d/tk8.6"
  tk_ok
}

# One-click Tk install so no-tk machines get the full window (with Custom tab)
# instead of the fallback dialogs. Returns 0 when tkinter is usable.
tk_pkg_for() {
  if have apt-get; then echo "apt-get:python3-tk"
  elif have dnf; then echo "dnf:python3-tkinter"
  elif have pacman; then echo "pacman:tk"
  elif have zypper; then echo "zypper:python3-tkinter"
  else echo ""; fi
}

ensure_tk() {
  tk_ok && return 0
  # Zero-install path first: bundled runtime, no admin, no downloads.
  try_bundle_tk && return 0
  [ -n "$(tk_pkg_for)" ] || return 1
  have zenity && has_display || return 1
  local spec pm pkgs
  spec="$(tk_pkg_for)"; pm="${spec%%:*}"; pkgs="${spec##*:}"
  zenity --question --title="ZenFox Setup" --width=540 \
    --text="The full setup window (with Custom mode) needs the Python Tk bundle, which is missing.\n\nInstall '$pkgs' now via $pm? One-time step, password is asked graphically.\n\nNo = continue with simple dialogs instead." \
    --ok-label="Install" --cancel-label="Use dialogs" || return 1
  have pkexec || {
    zenity --error --title="ZenFox Setup" --width=480 \
      --text="No graphical admin tool (pkexec) found.\nInstall '$pkgs' manually, then re-run setup.sh." || true
    return 1
  }
  case "$pm" in
    apt-get) pkexec apt-get install -y "$pkgs" ;;
    dnf) pkexec dnf install -y "$pkgs" ;;
    pacman) pkexec pacman -S --noconfirm "$pkgs" ;;
    zypper) pkexec zypper install -y "$pkgs" ;;
  esac >/dev/null 2>&1 || {
    zenity --error --title="ZenFox Setup" --width=480 \
      --text="Install failed. Continue with dialogs, or install '$pkgs' manually." || true
    return 1
  }
  tk_ok
}

open_terminal_fallback() {
  local cmd="python3 '$PWD/setup.py'; echo; read -n1 -r -p 'Press any key to close…'"
  if have x-terminal-emulator; then exec x-terminal-emulator -e bash -c "$cmd"
  elif have gnome-terminal; then exec gnome-terminal -- bash -c "$cmd"
  elif have konsole; then exec konsole -e bash -c "$cmd"
  elif have xfce4-terminal; then exec xfce4-terminal -e bash -c "$cmd"
  elif have xterm; then exec xterm -e bash -c "$cmd"
  elif have foot; then exec foot bash -c "$cmd"
  else
    have notify-send && notify-send "ZenFox Setup" "No GUI or terminal found. Run: python3 setup.py" >/dev/null 2>&1 || true
    echo "ERROR: no GUI (PySide6/tkinter/zenity) and no terminal found. Run: python3 setup.py" >&2
    exit 2
  fi
}

# One-click PySide6 install so machines with neither Qt nor Tk still get the
# full window. Tries user-level pip first, then a private .qt-venv (works on
# externally-managed Pythons like Arch where pip --user is blocked).
# Any failure shows the REAL log tail — never a guessed cause.
# Returns 0 when a GUI backend is usable.
offer_qt_pip() {
  qt_ok || tk_ok && return 0
  have zenity && has_display || return 1
  zenity --question --title="ZenFox Setup" --width=560 \
    --text="The full setup window needs PySide6 (Qt), which is missing.\n\nInstall it now? Files go to user space only (.qt-venv next to setup.sh or a pip user install) — no admin password. Needs internet once.\n\nNo = continue with the fallback options instead." \
    --ok-label="Install" --cancel-label="Skip" || return 1
  local log venv_py
  log="$(mktemp -t zenfox-qt-XXXXXX.log)" || return 1
  venv_py="$PWD/.qt-venv/bin/python"
  if python3 -m pip install -q --user PySide6 >"$log" 2>&1 && qt_ok; then
    rm -f "$log"
    return 0
  fi
  # NOTE: the venv check below must test the VENV interpreter, not system
  # python3 — system python never sees venv packages (that wrong check was
  # the "Qt install failed" false alarm on managed distros like Arch).
  if python3 -m venv "$PWD/.qt-venv" >>"$log" 2>&1 \
     && "$PWD/.qt-venv/bin/python" -m pip install -q PySide6 >>"$log" 2>&1 \
     && "$PWD/.qt-venv/bin/python" -c "import PySide6" >/dev/null 2>&1; then
    touch "$PWD/.qt-venv/.zenfox-qt-ready" 2>/dev/null || true
    rm -f "$log"
    return 0
  fi
  zenity --error --title="ZenFox Setup" --width=600 \
    --text="Qt install failed. Last output:\n$(tail -n6 "$log")\n\nFull log: $log\nContinuing with the fallback. Manual options: Arch 'sudo pacman -S pyside6', or run: python3 setup.py --gui" || true
  return 1
}

# macOS: .command files open in Terminal.app; prefer the Qt GUI inside it? No —
# detached GUI is nicer when a display exists and a backend works.
if has_display; then
  offer_qt_pip || true   # decline/failure falls through to Tk below
  ensure_tk || true  # decline/failure falls through to dialogs below
fi
# A verified .qt-venv counts as a GUI backend even when system python has
# neither Qt nor Tk — and its interpreter is what launches the new UI.
if has_display && { gui_ok || venv_ready; }; then
  # Detached: no terminal window stays open.
  _py="$(gui_python)"
  if have nohup; then
    nohup "$_py" setup.py --gui >/dev/null 2>&1 &
  else
    "$_py" setup.py --gui >/dev/null 2>&1 &
  fi
  exit 0
fi

if has_display && have zenity; then
  exec bash tools/gui_zenity.sh
fi

# Terminals need a display too — without one, fail fast with a clear message
# instead of letting each emulator crash.
if ! has_display; then
  echo "ERROR: no graphical session detected and no action possible non-interactively." >&2
  echo "Run one of:  python3 setup.py --help   |   python3 setup.py --preset zenfox --profile <name> --yes" >&2
  exit 2
fi

open_terminal_fallback
