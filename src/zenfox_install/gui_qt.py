"""ZenFox graphical setup — PySide6 (Qt-first UI).

Importing this module is safe without PySide6: the pure operation helpers
(do_install/do_compare/do_revert/do_apply_custom) are headless-safe and unit
tested. MainWindow raises a clear error if PySide6 is missing. Used by:
  python3 setup.py --gui        (Qt first, tkinter fallback if missing)
"""
import types
from pathlib import Path

from . import info, install, policies, profiles
from .gui import custom_log_line, describe_preset, make_zen_args, validate_inputs

try:
    from PySide6.QtCore import QObject, Qt, QThread, Signal
    from PySide6.QtGui import QColor, QPalette
    from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                                   QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                                   QMainWindow, QMessageBox, QPlainTextEdit, QPushButton,
                                   QRadioButton, QSplitter, QTabWidget, QVBoxLayout,
                                   QWidget)
    _QT = True
except ImportError:
    _QT = False


def need_qt():
    if not _QT:
        raise RuntimeError("PySide6 is not installed. Install it with:\n"
                           "  pip install PySide6")


def available():
    """True when the Qt backend can run (PySide6 importable)."""
    return _QT


# ---------------------------------------------------------- operations (pure)

def _check_profile(emit, profile):
    """Shared guards: valid dir + Firefox closed. Returns False to abort."""
    if not profile.is_dir():
        emit("ERROR: Pick a valid Firefox profile folder.")
        return False
    if install.firefox_lock_present(profile):
        emit("WARNING: Firefox looks open — close it first, then retry.")
        return False
    return True


def do_compare(emit, preset, profile, adv_level):
    """Compare ZenFox vs AdvancedFox prefs (no changes)."""
    from . import cli
    if not _check_profile(emit, profile):
        return
    errs = validate_inputs(preset, str(profile))
    if errs:
        emit("ERROR:\n- " + "\n- ".join(errs))
        return
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        if preset == "zenfox":
            args = make_zen_args()
            zsrc, _ = cli.resolve_zen_files(args, tmp)
            zen = info.parse_user_prefs((Path(zsrc) / "user.js").read_text())
            emit(f"ZenFox active prefs: {len(zen)}")
        else:
            zen = None
        ns = types.SimpleNamespace(adv_url=info.ADV_DEFAULT_URL,
                                   adv_sha256=None,
                                   adv_level=adv_level)
        asrc, _ = cli.resolve_adv_files(ns, tmp)
        adv = info.parse_user_prefs((Path(asrc) / "user.js").read_text())
        if zen is None:
            emit(f"AdvancedFox {adv_level} active prefs: {len(adv)}")
        else:
            emit(info.format_diff(info.diff_keys(zen, adv)))


def do_revert(emit, profile):
    """Restore the latest zenfox-backup-* in the profile."""
    backs = sorted(profile.glob("zenfox-backup-*"))
    if not backs:
        emit("ERROR: no zenfox-backup-* found in this profile.")
        return
    install.revert_backup(profile, backs[-1])
    emit(f"Restored {backs[-1].name}. Restart Firefox.")


def do_apply_custom(emit, profile, enabled_user, enabled_lite, secs_user, secs_lite):
    """Install a custom section selection. enabled_lite=None skips LiteFox."""
    from . import cli, sections
    if not _check_profile(emit, profile):
        return
    en_u = {t for t, v in enabled_user.items() if v}
    en_l = ({t for t, v in enabled_lite.items() if v}
            if enabled_lite is not None else None)
    if not en_u:
        emit("ERROR: at least one user.js section must stay ON.")
        return
    if enabled_lite is not None and not en_l:
        emit("ERROR: LiteFox include is ON but all its sections are OFF.")
        return
    import tempfile
    backup = install.backup_profile(profile)
    emit(f"Backup: {backup}")
    custom = cli.build_custom_files(cli.repo_root(), ",".join(sorted(en_u)),
                                    ",".join(sorted(en_l)) if en_l is not None else None)
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "custom"
        src.mkdir()
        for name, content in custom.items():
            (src / name).write_text(content, encoding="utf-8")
        done = install.install_files(src, profile, list(custom))
    emit(f"Custom installed into {profile}: {', '.join(done)} "
         f"({sections.count_active(secs_user, en_u)} user.js prefs"
         + (", LiteFox included" if en_l is not None else ", LiteFox skipped")
         + "). Restart Firefox.")


def do_install(emit, preset, profile, with_lite=False, with_soft=False,
               with_policies=False, adv_level="medium"):
    """Simple-tab install (preset + options). Never touches widgets."""
    from . import cli
    if not _check_profile(emit, profile):
        return
    errs = validate_inputs(preset, str(profile))
    if errs:
        emit("ERROR:\n- " + "\n- ".join(errs))
        return
    import tempfile
    backup = install.backup_profile(profile)
    emit(f"Backup: {backup}")
    with tempfile.TemporaryDirectory() as tmp:
        if preset == "zenfox":
            args = make_zen_args(with_lite, with_soft)
            src, files = cli.resolve_zen_files(args, tmp)
        else:
            ns = types.SimpleNamespace(adv_url=info.ADV_DEFAULT_URL,
                                       adv_sha256=None,
                                       adv_level=adv_level)
            src, files = cli.resolve_adv_files(ns, tmp)
        done = install.install_files(src, profile, files)
    if with_policies:
        if not policies.is_admin():
            emit("Skipped policies.json: needs admin rights.")
        else:
            import platform
            os_name = {"Windows": "windows", "Darwin": "macos"}.get(platform.system(), "linux")
            dest = policies.distribution_dirs(os_name)[0]
            if preset == "advancedfox":
                src_pol = info.adv_vendor_policies(cli.repo_root(), adv_level)
            else:
                src_pol = cli.repo_root() / "policies.json"
            policies.install_policies(src_pol, dest)
            emit(f"policies.json -> {dest}")
    emit(f"Installed into {profile}: {', '.join(done)}. Restart Firefox.")


# ---------------------------------------------------------------- Qt window

def apply_dark(app):
    """Fusion + dark palette. Qt-native smooth scrolling needs no helpers."""
    need_qt()
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor("#1e1e2e"))
    pal.setColor(QPalette.WindowText, QColor("#cdd6f4"))
    pal.setColor(QPalette.Base, QColor("#11111b"))
    pal.setColor(QPalette.AlternateBase, QColor("#1e1e2e"))
    pal.setColor(QPalette.Text, QColor("#cdd6f4"))
    pal.setColor(QPalette.Button, QColor("#2a2739"))
    pal.setColor(QPalette.ButtonText, QColor("#ece8f5"))
    pal.setColor(QPalette.Highlight, QColor("#ff7139"))
    pal.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)


if _QT:
    class _Worker(QObject):
        log = Signal(str)
        finished = Signal()

        def __init__(self, fn):
            super().__init__()
            self._fn = fn

        def run(self):
            try:
                self._fn(self.log.emit)
            except Exception as e:  # show, never crash silently
                self.log.emit(f"ERROR: {e}")
            finally:
                self.finished.emit()


    class MainWindow(QMainWindow):
        def __init__(self, initial_tab="simple"):
            super().__init__()
            self.setWindowTitle("ZenFox Setup")
            self.resize(1000, 720)
            self._threads = []
            self._workers = []  # ownership: thread/objects die only via finished chain
            self.custom_state = {"loaded": False, "user": [], "lite": [],
                                 "enabled_user": {}, "enabled_lite": {},
                                 "detail_title": None}

            central = QWidget()
            self.setCentralWidget(central)
            layout = QVBoxLayout(central)

            banner = QLabel("  ZenFox Setup  ·  offline presets for Firefox — Simple + Custom")
            banner.setStyleSheet("background: #ff7139; color: white; font-weight: bold;"
                                 " font-size: 14px; padding: 8px;")
            layout.addWidget(banner)

            layout.addWidget(QLabel("Firefox profile"))
            prof_row = QHBoxLayout()
            layout.addLayout(prof_row)
            self.profile_combo = QComboBox()
            self.profile_combo.setEditable(True)
            self.profile_combo.setMinimumWidth(400)
            prof_row.addWidget(self.profile_combo, stretch=1)
            self._found = []
            self.reload_profiles()
            for text, slot in (("Browse…", self.browse_profile),
                               ("Create new…", self.create_profile),
                               ("Refresh", self.reload_profiles)):
                btn = QPushButton(text)
                btn.clicked.connect(slot)
                prof_row.addWidget(btn)

            self.tabs = QTabWidget()
            layout.addWidget(self.tabs, stretch=1)
            self._build_simple_tab()
            self._build_custom_tab()
            if initial_tab == "custom":
                self.tabs.setCurrentIndex(1)
            self.tabs.currentChanged.connect(self._on_tab_changed)

            layout.addWidget(QLabel("Log"))
            self.log_box = QPlainTextEdit()
            self.log_box.setReadOnly(True)
            self.log_box.setMaximumBlockCount(2000)
            layout.addWidget(self.log_box)

            btns = QHBoxLayout()
            layout.addLayout(btns)
            btns.addStretch(1)
            cmp_btn = QPushButton("Compare (no changes)")
            cmp_btn.clicked.connect(lambda: self.run("compare"))
            btns.addWidget(cmp_btn)
            inst_btn = QPushButton("Install")
            inst_btn.setStyleSheet("background: #ff7139; color: white; font-weight: bold;"
                                   " padding: 8px 18px;")
            inst_btn.clicked.connect(lambda: self.run("install", confirm=True))
            btns.addWidget(inst_btn)
            rev_btn = QPushButton("Revert latest backup")
            rev_btn.clicked.connect(lambda: self.run("revert", confirm=True))
            btns.addWidget(rev_btn)

        # --- profile row ---
        def reload_profiles(self):
            self._found = profiles.list_profiles()
            labels = [f"{p['name']}{' (default)' if p['is_default'] else ''} — {p['path']}"
                      for p in self._found]
            cur = self.profile_combo.currentText()
            self.profile_combo.clear()
            self.profile_combo.addItems(labels or ["(no profiles found — Browse…)"])
            if cur:
                self.profile_combo.setCurrentText(cur)

        def browse_profile(self):
            d = QFileDialog.getExistingDirectory(self, "Pick Firefox profile folder")
            if d:
                self.profile_combo.setCurrentText(d)

        def create_profile(self):
            try:
                created = profiles.create_profile(
                    profiles.choose_creation_root(profiles.data_roots()))
            except Exception as e:
                QMessageBox.critical(self, "ZenFox Setup", f"Could not create profile:\n{e}")
                return
            self.reload_profiles()
            for i in range(self.profile_combo.count()):
                if str(created["path"]) in self.profile_combo.itemText(i):
                    self.profile_combo.setCurrentIndex(i)
                    break

        def selected_profile(self):
            sel = self.profile_combo.currentText()
            for p in self._found:
                for i in range(self.profile_combo.count()):
                    if (self.profile_combo.itemText(i) == sel
                            and str(p["path"]) in sel):
                        return str(p["path"])
            return sel.strip()

        # --- simple tab ---
        def _build_simple_tab(self):
            tab = QWidget()
            self.tabs.addTab(tab, "Simple")
            layout = QVBoxLayout(tab)
            layout.addWidget(QLabel("1. Choose preset"))
            self.preset_zen = QRadioButton("ZenFox v157 Balanced — everyday speed (recommended)")
            self.preset_adv = QRadioButton("AdvancedFox 1.0.0 — perf + hardening (breaks more sites)")
            self.preset_zen.setChecked(True)
            self.preset_zen.toggled.connect(self.refresh_info)
            layout.addWidget(self.preset_zen)
            layout.addWidget(self.preset_adv)
            self.info_box = QPlainTextEdit()
            self.info_box.setReadOnly(True)
            self.info_box.setMaximumBlockCount(100)
            layout.addWidget(self.info_box)
            self.refresh_info()
            adv_row = QHBoxLayout()
            layout.addLayout(adv_row)
            adv_row.addWidget(QLabel("AdvancedFox level (vendored, offline):"))
            self.adv_level = QComboBox()
            self.adv_level.addItems(["weak", "medium", "strong"])
            self.adv_level.setCurrentText("medium")
            adv_row.addWidget(self.adv_level)
            adv_row.addStretch(1)
            note = QLabel("Custom upstream .zip? Use CLI flags --adv-url/--adv-sha256.")
            note.setStyleSheet("color: gray; font-size: 9pt;")
            layout.addWidget(note)
            layout.addWidget(QLabel("2. Options (ZenFox only)"))
            self.lite_check = QCheckBox("Also install LiteFox.js (debloat/UI)")
            self.soft_check = QCheckBox("Also install Softfox.js (ZEN smooth scroll)")
            self.pol_check = QCheckBox("Install policies.json (needs admin)")
            layout.addWidget(self.lite_check)
            layout.addWidget(self.soft_check)
            layout.addWidget(self.pol_check)
            layout.addStretch(1)

        def selected_preset(self):
            return "advancedfox" if self.preset_adv.isChecked() else "zenfox"

        def refresh_info(self):
            self.info_box.setPlainText(describe_preset(self.selected_preset()))

        # --- custom tab ---
        def _build_custom_tab(self):
            tab = QWidget()
            self.tabs.addTab(tab, "Custom")
            layout = QVBoxLayout(tab)
            top = QHBoxLayout()
            layout.addLayout(top)
            self.include_lite = QCheckBox("Install LiteFox.js too (section toggles below)")
            top.addWidget(self.include_lite)
            self.count_label = QLabel("0/0 sections")
            top.addWidget(self.count_label)
            top.addStretch(1)
            reset_btn = QPushButton("Clear log (reset all ON)")
            reset_btn.clicked.connect(self.reset_custom_log)
            top.addWidget(reset_btn)

            split = QSplitter(Qt.Horizontal)
            layout.addWidget(split, stretch=1)
            self.section_list = QListWidget()
            self.section_list.itemClicked.connect(
                lambda item: self.show_detail(item.data(Qt.UserRole)))
            self.section_list.itemChanged.connect(self._on_item_changed)
            split.addWidget(self.section_list)
            self.detail_box = QPlainTextEdit()
            self.detail_box.setReadOnly(True)
            split.addWidget(self.detail_box)
            self.changelog_box = QPlainTextEdit()
            self.changelog_box.setReadOnly(True)
            split.addWidget(self.changelog_box)
            split.setSizes([300, 380, 320])

            apply_btn = QPushButton("apply changes")
            apply_btn.setStyleSheet("background: #ff7139; color: white; font-weight: bold;"
                                    " padding: 8px 18px;")
            apply_btn.clicked.connect(lambda: self.run("apply-custom", confirm=True))
            row = QHBoxLayout()
            row.addStretch(1)
            row.addWidget(apply_btn)
            layout.addLayout(row)

        def _on_tab_changed(self, index):
            if index == 1:
                self.load_custom()

        def load_custom(self):
            if self.custom_state["loaded"]:
                return
            from . import sections
            from . import cli
            try:
                _, self.custom_state["user"] = sections.parse_file(cli.repo_root() / "user.js")
                _, self.custom_state["lite"] = sections.parse_file(cli.repo_root() / "LiteFox.js")
            except Exception as e:
                self.changelog_box.appendPlainText(f"ERROR loading preset files: {e}")
                return
            self.section_list.blockSignals(True)
            try:
                for sec in self.custom_state["user"]:
                    self.custom_state["enabled_user"][sec["title"]] = True
                for sec in self.custom_state["lite"]:
                    self.custom_state["enabled_lite"][sec["title"]] = True
                for sec in self.custom_state["user"] + self.custom_state["lite"]:
                    item = QListWidgetItem(f"▶ {sec['title']} ({len(sec['prefs'])})")
                    item.setData(Qt.UserRole, sec["title"])
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    if sec["empty"]:
                        item.setCheckState(Qt.Unchecked)
                        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                        key = ("enabled_lite" if sec["file"] == "LiteFox.js"
                               else "enabled_user")
                        self.custom_state[key][sec["title"]] = False
                    else:
                        item.setCheckState(Qt.Checked)
                    self.section_list.addItem(item)
            finally:
                self.section_list.blockSignals(False)
            self.custom_state["loaded"] = True
            self.changelog_box.appendPlainText(
                "Custom mode ready: all sections ON (= stock preset). Uncheck to exclude.")
            self.update_count()
            self.show_detail(None)

        def _on_item_changed(self, item):
            title = item.data(Qt.UserRole)
            sec = next((s for s in self.custom_state["user"] + self.custom_state["lite"]
                        if s["title"] == title), None)
            if sec is None:
                return
            on = item.checkState() == Qt.Checked
            if sec["file"] == "user.js":
                self.custom_state["enabled_user"][title] = on
            else:
                self.custom_state["enabled_lite"][title] = on
            self.changelog_box.appendPlainText(custom_log_line(sec, on))
            self.update_count()

        def update_count(self):
            nu = sum(1 for v in self.custom_state["enabled_user"].values() if v)
            nl = sum(1 for v in self.custom_state["enabled_lite"].values() if v)
            total = len(self.custom_state["enabled_user"]) + len(self.custom_state["enabled_lite"])
            self.count_label.setText(f"{nu + nl}/{total} sections")

        def reset_custom_log(self):
            secs = self.custom_state["user"] + self.custom_state["lite"]
            self.section_list.blockSignals(True)
            try:
                for i, sec in enumerate(secs):
                    keep_on = not sec["empty"]
                    self.section_list.item(i).setCheckState(
                        Qt.Checked if keep_on else Qt.Unchecked)
                    key = ("enabled_lite" if sec["file"] == "LiteFox.js"
                           else "enabled_user")
                    self.custom_state[key][sec["title"]] = keep_on
            finally:
                self.section_list.blockSignals(False)
            self.changelog_box.clear()
            self.changelog_box.appendPlainText("Reset: all sections ON (= stock preset).")
            self.update_count()
            self.show_detail(self.custom_state["detail_title"])

        def show_detail(self, title):
            self.custom_state["detail_title"] = title
            if not title:
                self.detail_box.setPlainText("Click ▶ on a section to preview its prefs.")
                return
            sec = next((s for s in self.custom_state["user"] + self.custom_state["lite"]
                        if s["title"] == title), None)
            if sec is None:
                return
            lines = [f"{sec['title']}  ({sec['file']})",
                     f"{len(sec['prefs'])} active prefs"]
            if sec["empty"]:
                lines.append("(empty — removed upstream, nothing to install)")
            lines.append("")
            for p in sec["prefs"]:
                line = f"• {p['key']} = {p['value']}"
                if p["comment"]:
                    line += f"  # {p['comment'][:80]}"
                lines.append(line)
            self.detail_box.setPlainText("\n".join(lines))

        # --- run ops in a worker thread (widgets snapshotted first) ---
        def append_log(self, msg):
            self.log_box.appendPlainText(msg)

        def run(self, mode, confirm=False):
            if confirm and QMessageBox.question(
                    self, "Confirm",
                    "Back up profile and install? Close Firefox first."
                    ) != QMessageBox.Yes:
                return
            profile = Path(self.selected_profile()).expanduser()
            if mode == "compare":
                fn = lambda emit: do_compare(emit, self.selected_preset(),
                                             profile, self.adv_level.currentText())
            elif mode == "revert":
                fn = lambda emit: do_revert(emit, profile)
            elif mode == "apply-custom":
                self.load_custom()
                en_u = dict(self.custom_state["enabled_user"])
                en_l = (dict(self.custom_state["enabled_lite"])
                        if self.include_lite.isChecked() else None)
                secs_u, secs_l = self.custom_state["user"], self.custom_state["lite"]
                fn = lambda emit: do_apply_custom(emit, profile, en_u, en_l, secs_u, secs_l)
            else:
                preset = self.selected_preset()
                lite, soft, pol = (self.lite_check.isChecked(), self.soft_check.isChecked(),
                                   self.pol_check.isChecked())
                level = self.adv_level.currentText()
                fn = lambda emit: do_install(emit, preset, profile, lite, soft, pol, level)
            thread = QThread(self)
            worker = _Worker(fn)
            worker.moveToThread(thread)
            worker.log.connect(self.append_log)
            thread.started.connect(worker.run)
            worker.finished.connect(thread.quit)
            worker.finished.connect(worker.deleteLater)
            thread.finished.connect(thread.deleteLater)
            self._threads.append(thread)
            self._workers.append(worker)
            thread.finished.connect(lambda: self._drop_worker(thread, worker))
            thread.start()

        def _drop_worker(self, thread, worker):
            if thread in self._threads:
                self._threads.remove(thread)
            if worker in self._workers:
                self._workers.remove(worker)

else:
    class MainWindow:  # noqa: D101 (placeholder when PySide6 is absent)
        def __init__(self, *a, **k):
            need_qt()


def main(initial_tab="simple"):
    """Open the Qt setup window."""
    need_qt()
    app = QApplication.instance() or QApplication([])
    apply_dark(app)
    win = MainWindow(initial_tab=initial_tab)
    win.show()
    app.exec()
