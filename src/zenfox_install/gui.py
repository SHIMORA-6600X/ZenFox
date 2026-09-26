"""ZenFox graphical setup — tkinter, lazy import.

Importing this module must NOT require tkinter (pure helpers are unit
tested headless). Only main() imports tkinter. Used by:
  python3 setup.py --gui        (or double-click setup.sh)
"""
import queue
import threading
import types
from pathlib import Path

from . import info, install, policies, profiles


# ---------------------------------------------------------------- pure helpers

def describe_preset(key):
    """Human-readable info card for the picker. Pure, headless-safe."""
    p = info.PRESETS[key]
    return (
        f"{p['name']}\n"
        f"Source: {p['source']}\n"
        f"Contents: {p['prefs']}\n"
        f"Best for: {p['best_for']}\n"
        f"Risk: {p['risk']}\n"
        f"Files: {', '.join(p['files'])}"
    )


def files_for_preset(preset, with_lite=False, with_soft=False):
    """Which repo files to install. AdvancedFox ships its own user.js only."""
    if preset == "advancedfox":
        return ["user.js"]
    files = ["user.js"]
    if with_lite:
        files.append("LiteFox.js")
    if with_soft:
        files.append("Softfox.js")
    return files


def validate_inputs(preset, profile, adv_url="", adv_sha256=""):
    """Return list of error strings (empty = OK). Pure, headless-safe.

    AdvancedFox installs from vendored files by default; a custom URL must be
    a hash-pinned .zip, anything else is rejected (no silent fallback).
    """
    from . import info as _info
    errors = []
    if preset not in ("zenfox", "advancedfox"):
        errors.append("Pick a preset: ZenFox or AdvancedFox.")
    if not profile or not Path(profile).expanduser().is_dir():
        errors.append("Pick a valid Firefox profile folder.")
    if preset == "advancedfox":
        url = (adv_url or "").strip()
        if url and url != _info.ADV_DEFAULT_URL:
            if not url.endswith(".zip"):
                errors.append("Custom AdvancedFox URL must be a release .zip (or leave default for vendored).")
            elif not (adv_sha256 or "").strip():
                errors.append("Custom AdvancedFox .zip needs its SHA256 hash (hash-pinned downloads only).")
    return errors


def custom_log_line(section, enabled):
    """One change-log line for a section toggle. Pure, headless-safe."""
    from . import sections as _sections
    return _sections.summarize(section, enabled)


# ---------------------------------------------------------------- smooth scrolling (headless-safe)

PX_PER_NOTCH = 104  # pixels glided per wheel notch at 1:1 (yscrollincrement=1)


class SmoothScroller:
    """Butter-smooth wheel glides. No tkinter import (inject widget + after).

    Notches accumulate (floats OK, e.g. macOS trackpads) into a pixel queue
    capped at ~3 notches; a ~15 ms loop drains it with exponential ease-out.
    Requires the widget at pixel granularity (canvas yscrollincrement=1).
    """

    def __init__(self, widget, after, px_per_notch=PX_PER_NOTCH):
        self._w = widget
        self._after = after
        self._px = px_per_notch
        self._queue = 0.0
        self._running = False

    def scroll(self, notches):
        self._queue += notches * self._px
        cap = self._px * 3
        self._queue = max(-cap, min(cap, self._queue))
        if not self._running and self._queue:
            self._running = True
            self._after(15, self._tick)

    def _tick(self):
        if not self._queue:
            self._running = False
            return
        step = int(self._queue * 0.35)  # ease-out: 35% of remainder
        if step == 0:
            step = 1 if self._queue > 0 else -1
        self._w.yview_scroll(step, "units")
        self._queue -= step
        self._after(15, self._tick)


def make_zen_args(with_lite=False, with_soft=False):
    from . import cli
    args = cli.build_parser().parse_args(["--preset", "zenfox"])
    args.with_lite = with_lite
    args.with_soft = with_soft
    return args


# ---------------------------------------------------------------- theme (headless-safe data + stub-safe applier)

THEME = {
    "bg": "#17141f",        # app background
    "surface": "#221f30",   # frames, panes, section rows
    "card": "#2a2739",      # buttons, dropdowns
    "entry": "#14121b",     # text fields / log panes
    "fg": "#ece8f5",        # main text
    "muted": "#a09ab5",     # secondary text
    "accent": "#ff7139",    # primary actions, highlights
    "accent_dark": "#d9531f",
    "accent_fg": "#ffffff",
    "ok": "#43c59e",
    "border": "#3b3752",
    "select": "#4a3f6e",    # text selection
}


def apply_theme(tk_mod, ttk_mod, root):
    """Dark modern theme, stdlib only. Safe to call with stub modules in tests."""
    t = THEME
    try:
        ttk_mod.Style().theme_use("clam")  # native-ish base on Linux
    except Exception:
        pass
    # tk widgets via the option database (applies to widgets created after).
    for pattern, value in (
        ("*Background", t["surface"]),
        ("*Foreground", t["fg"]),
        ("*Button.background", t["card"]),
        ("*Button.foreground", t["fg"]),
        ("*Button.activeBackground", t["border"]),
        ("*Button.activeForeground", t["fg"]),
        ("*Checkbutton.background", t["surface"]),
        ("*Checkbutton.foreground", t["fg"]),
        ("*Checkbutton.activeBackground", t["surface"]),
        ("*Checkbutton.selectColor", t["entry"]),
        ("*Radiobutton.background", t["surface"]),
        ("*Radiobutton.foreground", t["fg"]),
        ("*Radiobutton.activeBackground", t["surface"]),
        ("*Radiobutton.selectColor", t["accent"]),
        ("*Label.background", t["surface"]),
        ("*Label.foreground", t["fg"]),
        ("*LabelFrame.background", t["surface"]),
        ("*LabelFrame.foreground", t["muted"]),
        ("*Text.background", t["entry"]),
        ("*Text.foreground", t["fg"]),
        ("*Text.insertBackground", t["accent"]),
        ("*Text.selectBackground", t["select"]),
        ("*Entry.background", t["entry"]),
        ("*Entry.foreground", t["fg"]),
        ("*Entry.insertBackground", t["accent"]),
        ("*Menubutton.background", t["card"]),
        ("*Menubutton.foreground", t["fg"]),
        ("*Menubutton.activeBackground", t["border"]),
        ("*Menu.background", t["card"]),
        ("*Menu.foreground", t["fg"]),
        ("*Menu.activeBackground", t["accent"]),
        ("*Canvas.background", t["surface"]),
        ("*Scrollbar.background", t["card"]),
        ("*Scrollbar.troughColor", t["bg"]),
    ):
        try:
            root.option_add(pattern, value)
        except Exception:
            pass
    # ttk widgets via styles.
    try:
        st = ttk_mod.Style()
        st.configure("TFrame", background=t["surface"])
        st.configure("TLabel", background=t["surface"], foreground=t["fg"])
        st.configure("TLabelFrame", background=t["surface"], foreground=t["muted"])
        st.configure("TButton", background=t["card"], foreground=t["fg"],
                     padding=(10, 6), borderwidth=0, focusthickness=0)
        st.map("TButton",
               background=[("active", t["border"]), ("pressed", t["border"])],
               foreground=[("active", t["fg"])])
        st.configure("Accent.TButton", background=t["accent"], foreground=t["accent_fg"],
                     padding=(14, 7), borderwidth=0, font=("TkDefaultFont", 9, "bold"))
        st.map("Accent.TButton",
               background=[("active", t["accent_dark"]), ("pressed", t["accent_dark"])],
               foreground=[("active", t["accent_fg"])])
        st.configure("TNotebook", background=t["bg"], borderwidth=0)
        st.configure("TNotebook.Tab", background=t["surface"], foreground=t["muted"],
                     padding=(14, 6), borderwidth=0)
        st.map("TNotebook.Tab",
               background=[("selected", t["card"])],
               foreground=[("selected", t["accent"])])
        st.configure("TCheckbutton", background=t["surface"], foreground=t["fg"])
        st.configure("TRadiobutton", background=t["surface"], foreground=t["fg"])
        st.configure("TEntry", fieldbackground=t["entry"], foreground=t["fg"],
                     insertcolor=t["accent"])
        st.configure("TMenubutton", background=t["card"], foreground=t["fg"],
                     arrowcolor=t["accent"])
        st.configure("TScrollbar", background=t["card"], troughcolor=t["bg"],
                     arrowcolor=t["muted"], borderwidth=0)
        st.configure("TPanedwindow", background=t["bg"])
        st.configure("TSeparator", background=t["border"])
    except Exception:
        pass


# ---------------------------------------------------------------- GUI (tkinter)

def main(initial_tab="simple"):
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext, ttk

    from . import cli, sections

    root = tk.Tk()
    root.title("ZenFox Setup")
    root.geometry("960x700")
    root.resizable(True, True)
    root.configure(bg=THEME["bg"])
    apply_theme(tk, ttk, root)

    # --- banner ----------------------------------------------------------
    banner = tk.Frame(root, bg=THEME["accent"])
    banner.pack(fill="x")
    tk.Label(banner, text="ZenFox Setup", bg=THEME["accent"], fg=THEME["accent_fg"],
             font=("TkDefaultFont", 13, "bold")).pack(side="left", padx=12, pady=6)
    tk.Label(banner, text="offline presets for Firefox  ·  Simple + Custom",
             bg=THEME["accent"], fg=THEME["accent_fg"],
             font=("TkDefaultFont", 9)).pack(side="left", padx=4)

    log_q = queue.Queue()

    # --- shared profile row (above tabs) ----------------------------------
    tk.Label(root, text="Firefox profile", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    prof_frame = tk.Frame(root)
    prof_frame.pack(fill="x", padx=10)
    found = profiles.list_profiles()
    labels = [f"{p['name']}{' (default)' if p['is_default'] else ''} — {p['path']}" for p in found]
    prof_var = tk.StringVar(value=labels[0] if labels else "(no profiles found — Browse…)")
    prof_menu = tk.OptionMenu(prof_frame, prof_var, *(labels or ["(no profiles found — Browse…)"]))
    prof_menu.pack(side="left", fill="x", expand=True)

    def reload_profiles():
        found.clear()
        found.extend(profiles.list_profiles())
        labels.clear()
        labels.extend(f"{p['name']}{' (default)' if p['is_default'] else ''} — {p['path']}" for p in found)
        menu = prof_menu["menu"]
        menu.delete(0, "end")
        for lab in (labels or ["(no profiles found — Browse…)"]):
            menu.add_command(label=lab, command=lambda v=lab: prof_var.set(v))
        prof_var.set(labels[0] if labels else "(no profiles found — Browse…)")

    def browse():
        d = filedialog.askdirectory(title="Pick Firefox profile folder")
        if d:
            prof_var.set(d)

    def create_new():
        try:
            created = profiles.create_profile(
                profiles.choose_creation_root(profiles.data_roots()))
        except Exception as e:
            messagebox.showerror("ZenFox Setup", f"Could not create profile:\n{e}")
            return
        reload_profiles()
        for lab in labels:
            if str(created["path"]) in lab:
                prof_var.set(lab)
                break

    ttk.Button(prof_frame, text="Browse…", command=browse).pack(side="left", padx=4)
    ttk.Button(prof_frame, text="Create new…", command=create_new).pack(side="left")
    ttk.Button(prof_frame, text="Refresh", command=reload_profiles).pack(side="left")

    def selected_profile():
        sel = prof_var.get()
        for p, lab in zip(found, labels):
            if sel == lab:
                return str(p["path"])
        return sel.strip()

    # --- tabs --------------------------------------------------------------
    tabs = ttk.Notebook(root)
    tabs.pack(fill="both", expand=True, padx=10, pady=6)
    simple_tab = tk.Frame(tabs)
    custom_tab = tk.Frame(tabs)
    tabs.add(simple_tab, text="Simple")
    tabs.add(custom_tab, text="Custom")

    # --- SIMPLE tab ----------------------------------------------------------
    preset_var = tk.StringVar(value="zenfox")
    tk.Label(simple_tab, text="1. Choose preset", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    info_box = tk.Text(simple_tab, height=8, wrap="word", relief="flat",
                   borderwidth=0, highlightthickness=1,
                   highlightbackground=THEME["border"])
    info_box.pack(fill="x", padx=10, pady=4)
    info_box.configure(state="disabled")

    def refresh_info(*_):
        info_box.configure(state="normal")
        info_box.delete("1.0", "end")
        info_box.insert("end", describe_preset(preset_var.get()))
        info_box.configure(state="disabled")

    for key, label in (("zenfox", "ZenFox v157 Balanced — everyday speed (recommended)"),
                       ("advancedfox", "AdvancedFox 1.0.0 — perf + hardening (breaks more sites)")):
        tk.Radiobutton(simple_tab, text=label, variable=preset_var, value=key,
                       command=refresh_info).pack(anchor="w", padx=20)
    refresh_info()

    adv_row = tk.Frame(simple_tab)
    adv_row.pack(fill="x", padx=10, pady=2)
    tk.Label(adv_row, text="AdvancedFox level (vendored, offline):").pack(side="left")
    adv_level_var = tk.StringVar(value="medium")
    tk.OptionMenu(adv_row, adv_level_var, "weak", "medium", "strong").pack(side="left", padx=4)
    tk.Label(simple_tab, text="Custom upstream .zip? Use CLI flags --adv-url/--adv-sha256.",
             font=("TkDefaultFont", 8), fg="gray").pack(anchor="w", padx=10)

    tk.Label(simple_tab, text="2. Options (ZenFox only)", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
    lite_var, soft_var, pol_var = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
    tk.Checkbutton(simple_tab, text="Also install LiteFox.js (debloat/UI)", variable=lite_var).pack(anchor="w", padx=20)
    tk.Checkbutton(simple_tab, text="Also install Softfox.js (ZEN smooth scroll)", variable=soft_var).pack(anchor="w", padx=20)
    tk.Checkbutton(simple_tab, text="Install policies.json (needs admin)", variable=pol_var).pack(anchor="w", padx=20)

    # --- CUSTOM tab: ZenFox Config | detail | change logs + Apply -------------
    custom_state = {"loaded": False, "user": [], "lite": [],
                    "enabled_user": {}, "enabled_lite": {},
                    "detail_title": None}

    custom_top = tk.Frame(custom_tab)
    custom_top.pack(fill="x", padx=6, pady=4)
    include_lite_var = tk.BooleanVar(value=False)
    tk.Checkbutton(custom_top, text="Install LiteFox.js too (section toggles below)",
                   variable=include_lite_var).pack(side="left")
    count_var = tk.StringVar(value="21/21 sections")
    tk.Label(custom_top, textvariable=count_var).pack(side="left", padx=12)
    ttk.Button(custom_top, text="Clear log (reset all ON)",
               command=lambda: reset_custom_log()).pack(side="right")

    panes = ttk.PanedWindow(custom_tab, orient="horizontal")
    panes.pack(fill="both", expand=True, padx=6, pady=2)

    left_frame = tk.LabelFrame(panes, text="ZenFox Config")
    center_frame = tk.LabelFrame(panes, text="Section")
    right_frame = tk.LabelFrame(panes, text="change logs")
    panes.add(left_frame, weight=3)
    panes.add(center_frame, weight=4)
    panes.add(right_frame, weight=3)

    left_canvas = tk.Canvas(left_frame, highlightthickness=0, borderwidth=0)
    left_canvas.configure(yscrollincrement=1)  # pixel granularity for glides
    left_scroll = tk.Scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
    left_inner = tk.Frame(left_canvas)
    left_inner.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
    left_canvas.create_window((0, 0), window=left_inner, anchor="nw")
    left_canvas.configure(yscrollcommand=left_scroll.set)
    left_canvas.pack(side="left", fill="both", expand=True)
    left_scroll.pack(side="right", fill="y")

    detail_box = tk.Text(center_frame, wrap="word", relief="flat",
                      borderwidth=0, highlightthickness=1,
                      highlightbackground=THEME["border"])
    detail_box.pack(fill="both", expand=True, padx=4, pady=4)
    detail_box.configure(state="disabled")

    changelog_box = tk.Text(right_frame, wrap="word", relief="flat",
                            borderwidth=0, highlightthickness=1,
                            highlightbackground=THEME["border"])
    changelog_box.pack(fill="both", expand=True, padx=4, pady=4)
    changelog_box.configure(state="disabled")

    def changelog_append(line):
        changelog_box.configure(state="normal")
        changelog_box.insert("end", line + "\n")
        changelog_box.see("end")
        changelog_box.configure(state="disabled")
        update_count()

    def update_count():
        nu = sum(1 for v in custom_state["enabled_user"].values() if v)
        nl = sum(1 for v in custom_state["enabled_lite"].values() if v)
        count_var.set(f"{nu + nl}/{len(custom_state['enabled_user']) + len(custom_state['enabled_lite'])} sections")

    def reset_custom_log():
        secs = custom_state["user"] + custom_state["lite"]
        for sec, var in zip(secs, row_vars):
            keep_on = not sec["empty"]
            var.set(keep_on)
            target = (custom_state["enabled_user"] if sec["file"] == "user.js"
                      else custom_state["enabled_lite"])
            target[sec["title"]] = keep_on
        changelog_box.configure(state="normal")
        changelog_box.delete("1.0", "end")
        changelog_box.configure(state="disabled")
        changelog_append("Reset: all sections ON (= stock preset).")
        show_detail(custom_state["detail_title"])

    row_vars = []

    def show_detail(title):
        custom_state["detail_title"] = title
        detail_box.configure(state="normal")
        detail_box.delete("1.0", "end")
        if not title:
            detail_box.insert("end", "Click ▶ on a section to preview its prefs.")
        else:
            sec = next((s for s in custom_state["user"] + custom_state["lite"] if s["title"] == title), None)
            if sec:
                detail_box.insert("end", f"{sec['title']}  ({sec['file']})\n{len(sec['prefs'])} active prefs")
                if sec["empty"]:
                    detail_box.insert("end", "\n(empty — removed upstream, nothing to install)")
                detail_box.insert("end", "\n\n")
                for p in sec["prefs"]:
                    line = f"• {p['key']} = {p['value']}"
                    if p["comment"]:
                        line += f"  # {p['comment'][:80]}"
                    detail_box.insert("end", line + "\n")
        detail_box.configure(state="disabled")

    def on_toggle(sec, var):
        on = bool(var.get())
        if sec["file"] == "user.js":
            custom_state["enabled_user"][sec["title"]] = on
        else:
            custom_state["enabled_lite"][sec["title"]] = on
        changelog_append(custom_log_line(sec, on))

    def load_custom():
        if custom_state["loaded"]:
            return
        try:
            _, custom_state["user"] = sections.parse_file(cli.repo_root() / "user.js")
            _, custom_state["lite"] = sections.parse_file(cli.repo_root() / "LiteFox.js")
        except Exception as e:
            changelog_append(f"ERROR loading preset files: {e}")
            return
        for sec in custom_state["user"]:
            custom_state["enabled_user"][sec["title"]] = True
        for sec in custom_state["lite"]:
            custom_state["enabled_lite"][sec["title"]] = True
        for sec in custom_state["user"] + custom_state["lite"]:
            row = tk.Frame(left_inner)
            row.pack(fill="x", padx=2, pady=1)
            var = tk.BooleanVar(value=True)
            row_vars.append(var)
            if sec["empty"]:
                var.set(False)
                custom_state["enabled_lite" if sec["file"] == "LiteFox.js" else "enabled_user"][sec["title"]] = False
            cb = tk.Checkbutton(row, variable=var,
                                command=lambda s=sec, v=var: on_toggle(s, v))
            if sec["empty"]:
                cb.configure(state="disabled")
            cb.pack(side="left")
            title_btn = tk.Button(row, text=f"▶ {sec['title']} ({len(sec['prefs'])})",
                                  anchor="w", relief="flat", cursor="hand2",
                                  command=lambda t=sec["title"]: show_detail(t))
            title_btn.pack(side="left", fill="x", expand=True)
            title_btn.bind("<Enter>", lambda _e, b=title_btn: b.configure(fg=THEME["accent"]))
            title_btn.bind("<Leave>", lambda _e, b=title_btn: b.configure(fg=THEME["fg"]))
        custom_state["loaded"] = True
        changelog_append("Custom mode ready: all sections ON (= stock preset). Uncheck to exclude.")
        update_count()
        show_detail(None)

    def on_tab_changed(_event):
        if tabs.index(tabs.select()) == 1:
            load_custom()

    tabs.bind("<<NotebookTabChanged>>", on_tab_changed)
    if initial_tab == "custom":
        try:
            tabs.select(custom_tab)
        except Exception:
            pass

    apply_row = tk.Frame(custom_tab)
    apply_row.pack(fill="x", padx=6, pady=4)
    ttk.Button(apply_row, text="apply changes", style="Accent.TButton",
               command=lambda: run("apply-custom", confirm=True)).pack(side="right")

    # --- shared install log + simple-tab buttons ------------------------------
    tk.Label(root, text="Log", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", padx=10)
    log = scrolledtext.ScrolledText(root, height=8, state="disabled",
                                      relief="flat", borderwidth=0,
                                      highlightthickness=1,
                                      highlightbackground=THEME["border"])
    log.pack(fill="both", expand=False, padx=10, pady=4)

    def emit(msg):
        log.configure(state="normal")
        log.insert("end", msg + "\n")
        log.see("end")
        log.configure(state="disabled")

    def pump():
        while True:
            try:
                emit(log_q.get_nowait())
            except queue.Empty:
                break
        root.after(120, pump)

    # --- butter-smooth wheel: one root-level router, hover-aware ---------------
    # Wheel events carry no target, so route by pointer position: the pane
    # under the cursor scrolls, others never hijack it. The section list
    # glides pixel-by-pixel (SmoothScroller); text panes step 3 lines.
    _glide = SmoothScroller(left_canvas, root.after)

    def _scroll_fn_for(x, y):
        try:
            path = str(root.winfo_containing(x, y))
        except Exception:
            return None
        while path:
            if path == str(left_frame):
                return ("glide",)
            if path in (str(center_frame), str(right_frame)):
                return ("lines", detail_box if path == str(center_frame) else changelog_box)
            if path == str(log) or path.startswith(str(log) + "."):
                return ("lines", log)
            path = path.rsplit(".", 1)[0] if "." in path else ""
        return None

    def _on_wheel(notches, x, y):
        target = _scroll_fn_for(x, y)
        if target is None:
            return None
        if target[0] == "glide":
            _glide.scroll(notches)
        else:
            _box = target[1]
            _box.yview_scroll(3 if notches > 0 else -3, "units")
        return "break"  # don't double-scroll (e.g. Text class bindings)

    import platform as _plat
    if _plat.system() == "Linux":
        root.bind_all("<Button-4>", lambda e: _on_wheel(-1, e.x_root, e.y_root))
        root.bind_all("<Button-5>", lambda e: _on_wheel(1, e.x_root, e.y_root))
    elif _plat.system() == "Darwin":
        root.bind_all("<MouseWheel>", lambda e: _on_wheel(e.delta / 120, e.x_root, e.y_root))
    else:
        def _win_wheel(e):
            d = int(e.delta / 120)
            return _on_wheel(d if d else (-1 if e.delta < 0 else 1), e.x_root, e.y_root)
        root.bind_all("<MouseWheel>", _win_wheel)

    def worker(mode):
        try:
            profile = Path(selected_profile()).expanduser()
            if not profile.is_dir():
                log_q.put("ERROR: Pick a valid Firefox profile folder.")
                return
            if install.firefox_lock_present(profile):
                log_q.put("WARNING: Firefox looks open — close it first, then retry.")
                return
            if mode == "compare":
                preset = preset_var.get()
                errs = validate_inputs(preset, str(profile))
                if errs:
                    log_q.put("ERROR:\n- " + "\n- ".join(errs))
                    return
                import tempfile
                with tempfile.TemporaryDirectory() as tmp:
                    if preset == "zenfox":
                        args = make_zen_args()
                        zsrc, _ = cli.resolve_zen_files(args, tmp)
                        zen = info.parse_user_prefs((Path(zsrc) / "user.js").read_text())
                        log_q.put(f"ZenFox active prefs: {len(zen)}")
                    else:
                        zen = None
                    ns = types.SimpleNamespace(adv_url=info.ADV_DEFAULT_URL,
                                               adv_sha256=None,
                                               adv_level=adv_level_var.get())
                    asrc, _ = cli.resolve_adv_files(ns, tmp)
                    adv = info.parse_user_prefs((Path(asrc) / "user.js").read_text())
                    if zen is None:
                        log_q.put(f"AdvancedFox {adv_level_var.get()} active prefs: {len(adv)}")
                    else:
                        log_q.put(info.format_diff(info.diff_keys(zen, adv)))
                return
            if mode == "revert":
                backs = sorted(profile.glob("zenfox-backup-*"))
                if not backs:
                    log_q.put("ERROR: no zenfox-backup-* found in this profile.")
                    return
                install.revert_backup(profile, backs[-1])
                log_q.put(f"Restored {backs[-1].name}. Restart Firefox.")
                return
            if mode == "apply-custom":
                load_custom()
                en_u = {t for t, v in custom_state["enabled_user"].items() if v}
                en_l = ({t for t, v in custom_state["enabled_lite"].items() if v}
                        if include_lite_var.get() else None)
                if not en_u:
                    log_q.put("ERROR: at least one user.js section must stay ON.")
                    return
                if include_lite_var.get() and not en_l:
                    log_q.put("ERROR: LiteFox include is ON but all its sections are OFF.")
                    return
                import tempfile
                backup = install.backup_profile(profile)
                log_q.put(f"Backup: {backup}")
                custom = cli.build_custom_files(cli.repo_root(), ",".join(sorted(en_u)),
                                                ",".join(sorted(en_l)) if en_l is not None else None)
                with tempfile.TemporaryDirectory() as tmp:
                    src = Path(tmp) / "custom"
                    src.mkdir()
                    for name, content in custom.items():
                        (src / name).write_text(content, encoding="utf-8")
                    done = install.install_files(src, profile, list(custom))
                log_q.put(f"Custom installed into {profile}: {', '.join(done)} "
                          f"({sections.count_active(custom_state['user'], en_u)} user.js prefs"
                          + (f", LiteFox included" if en_l is not None else ", LiteFox skipped") + "). Restart Firefox.")
                return
            # install (simple)
            preset = preset_var.get()
            errs = validate_inputs(preset, str(profile))
            if errs:
                log_q.put("ERROR:\n- " + "\n- ".join(errs))
                return
            import tempfile
            backup = install.backup_profile(profile)
            log_q.put(f"Backup: {backup}")
            with tempfile.TemporaryDirectory() as tmp:
                if preset == "zenfox":
                    args = make_zen_args(lite_var.get(), soft_var.get())
                    src, files = cli.resolve_zen_files(args, tmp)
                else:
                    ns = types.SimpleNamespace(adv_url=info.ADV_DEFAULT_URL,
                                               adv_sha256=None,
                                               adv_level=adv_level_var.get())
                    src, files = cli.resolve_adv_files(ns, tmp)
                done = install.install_files(src, profile, files)
            if pol_var.get():
                if not policies.is_admin():
                    log_q.put("Skipped policies.json: needs admin rights.")
                else:
                    import platform
                    os_name = {"Windows": "windows", "Darwin": "macos"}.get(platform.system(), "linux")
                    dest = policies.distribution_dirs(os_name)[0]
                    if preset == "advancedfox":
                        src_pol = info.adv_vendor_policies(cli.repo_root(), adv_level_var.get())
                    else:
                        src_pol = cli.repo_root() / "policies.json"
                    policies.install_policies(src_pol, dest)
                    log_q.put(f"policies.json -> {dest}")
            log_q.put(f"Installed into {profile}: {', '.join(done)}. Restart Firefox.")
        except Exception as e:  # show, never crash silently
            log_q.put(f"ERROR: {e}")

    def run(mode, confirm=False):
        if confirm and not messagebox.askyesno(
                "Confirm", "Back up profile and install? Close Firefox first."):
            return
        threading.Thread(target=worker, args=(mode,), daemon=True).start()

    btns = tk.Frame(root)
    btns.pack(pady=6)
    ttk.Button(btns, text="Compare (no changes)", command=lambda: run("compare")).pack(side="left", padx=4)
    ttk.Button(btns, text="Install", style="Accent.TButton", command=lambda: run("install", confirm=True)).pack(side="left", padx=4)
    ttk.Button(btns, text="Revert latest backup", command=lambda: run("revert", confirm=True)).pack(side="left", padx=4)

    root.after(120, pump)
    root.mainloop()
