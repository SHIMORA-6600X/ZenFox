# Bundled Tcl/Tk runtime (Linux x86_64 only)

## Why
The graphical setup (`setup.py --gui`, `setup.sh` double-click) needs tkinter.
Many minimal distros ship Python **without** Tk, and some users cannot install
system packages. This directory vendors the exact shared libraries + script
files so the window works with zero installs.

Precedence at launch: system tkinter → bundled here → offer one-click
system install → zenity dialogs → terminal. Nothing here affects Windows or
macOS (their Python bundles include Tk). Frozen exes are NOT covered: they
rely on the build host's Tk (see tools/build_installer.py).

## Contents
- `linux-x86_64/`: `libtcl8.6.so`, `libtk8.6.so`, `tcl8.6/`, `tk8.6/` (~7 MB)
- `licenses/`: upstream license terms (Tcl/Tk BSD-style, see below)

## Provenance
Extracted from Artix world repo packages `tcl-8.6.16-1` + `tk-8.6.16-1`
(same 8.6 ABI that distro `python3-tk` packages use):
- `licenses/license.terms` ← tcl package `usr/share/licenses/tcl/license.terms`
- `licenses/tk-license.terms` ← tk package `usr/share/licenses/tk/license.terms`

Full license text: https://www.tcl.tk/software/tcltk/license.html

## Updating
1. Download newer `tcl`/`tk` 8.6.x packages for the target arch.
2. Replace `linux-x86_64/` contents (keep layout: two `.so` files + `tcl8.6/` + `tk8.6/`).
3. Refresh `licenses/` from the packages.
4. Verify: `env -u LD_LIBRARY_PATH -u TCL_LIBRARY -u TK_LIBRARY <setup.sh mechanism>`
   then `python3 setup.py --gui` on a tk-less machine.
5. Stay on 8.6.x: CPython's `_tkinter` links `libtk8.6.so` by SONAME.
