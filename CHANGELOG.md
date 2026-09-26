# Changelog

All notable changes to ZenFox presets are documented here.
Format follows Keep a Changelog. Versions are single-source in `VERSION`.

## [157] - 2026-09-26 — Balanced defaults, Custom mode, offline AdvancedFox, Qt GUI

### Added (presets: Custom mode + offline AdvancedFox)
- Vendored AdvancedFox 1.0.0 (`vendor/advancedfox/`, 6 per-OS level files + 3 policies + `VENDOR.md` provenance). Both presets install with zero downloads.
- `--adv-level weak|medium|strong` (default medium, per-OS file auto-picked; macOS uses linux variant).
- Custom mode: per-`SECTION:` on/off for `user.js` (9) + `LiteFox.js` (12) — new `sections.py` parser/generator, GUI `Simple|Custom` tabs (section list + preview + change log + `apply changes`), `--sections`/`--lite-sections`/`--list-sections` CLI flags, zenity section checklists.
- `profiles.create_profile()` + `--create-profile` + GUI/Zenity create flows (first profile becomes Default, never steals existing default).

### Added (Qt GUI + offline installer)
- PySide6 Qt interface (`src/zenfox_install/gui_qt.py`, Qt-first with automatic `.qt-venv` bootstrap, tkinter fallback): Simple|Custom tabs, 21-section picker with live preview + change log, threaded worker, dark theme.
- `tools/build_installer.py` (PyInstaller one-file, tkinter excluded) + per-OS release workflows (`release-{windows,linux,macos}.yml`): `ZenFox-Setup-Windows.exe`, `ZenFox-Setup-Linux`, `ZenFox-Setup-macOS` built, smoke-tested, and attached on `v*` tags.
- Double-click launchers (`setup.sh`/`setup.bat`): frozen bare launch opens the GUI; dead-stdin aborts cleanly (exit 1), Ctrl+C exits 130.
- 79-test suite green on Linux, Qt-venv, and Windows-under-Wine (venv-marker, bare-launch, EOF guards).

### Fixed (installer)
- `sections.py` banner-boundary bug (section raw could swallow next banner → unclosed comment); exhaustive single-section `node --check` regression test.
- CLI validates `--sections` before backup (fail-fast, no side effects); latent `sources` NameError in `cli.py` fixed.
- Zenity no-profiles placeholder leak; stale AdvancedFox download prompts replaced by level picker.
- Bare-launch `EOFError` dialog (frozen double-click with no console); venv-marker false negatives on CI runners and Windows (`bin` vs `Scripts` layout).

### Presets — Balanced defaults + critical fixes (2026-09-25)

#### Fixed (P0)
- `user.js`: removed stray `/` line that caused `SyntaxError` and disabled the entire preset.
- `Softfox.js`: only ONE scroll profile active by default (ZEN SMOOTH). Other four options commented with `[PICK ONE]` instructions + reset procedure. Previously all five were active and overwrote each other.
- `LiteFox.js`: added missing `;` on `layout.css.prefers-color-scheme.content-override`; deduped `browser.urlbar.suggest.engines`.
- URLs: `Softfox.js` header and `README.md` license link now point to `ZenFox`, not `NitroFox`.

#### Changed (Balanced v157 — safe defaults)
- `user.js` network: `max-connections 1800→900`, pacing `disabled→enabled` (6/10), DNS expiration `3600→360`, grace `120→60`, entries `1600→1000`.
- `user.js` cache: disk `1024000→512000` (512MB), media combined `1048576→524288`, readahead `3600→60`, resume `1800→30`, storage quota `20480→10240`.
- `user.js` tab unload: `low_commit_space_threshold_mb 3276→200` (default; set per-RAM only as opt-in).
- `user.js` TLS token cache: reverted to Firefox default (commented out).
- `LiteFox.js` fullscreen: `warning.timeout 0→1250`, `warning.delay -1→500` (safe; 0/-1 is unsafe opt-in only).
- `LiteFox.js` Pocket prefs: commented out (Pocket removed from modern Firefox).
- `user.js` legacy prefs commented out: `content.notify.*`, `content.max.tokenizing.time`, `content.interrupt.parsing`, `content.switch.threshold`, `smart_size`, `delay_in_oopif`, `max_entries`, `high_water_mark`, `max_decoded_image_kb`.
- `policies.json`: removed `WebsiteFilter Block localhost/*` (broke dev), cleaned empty DoH `ProviderURL`, documented forced uBlock install, added version comment.

#### Added
- `VERSION` (single source), `tools/lint.sh`, `tools/build.sh`, CI workflow, `.gitignore`, `docs/benchmarks.md` placeholder.
- `README.md`: file matrix, Firefox support range, uninstall/revert instructions, release contents.
- `docs/index.html`: code samples synced to shipped values (no more `pipelining:true`).

#### Notes
- `user.js` prefs persist in `prefs.js` after deleting `user.js`. To fully revert: `about:support > Refresh Firefox` or restore backup profile.
- Aggressive `Max` values from v152 are preserved in comments as `Max opt-in` for users who benchmark them.

## [156] - prior — LiteFox debloat iteration
- LiteFox UI/AI/translations/newtab/urlbar hardening.

## [152] - prior — Initial performance presets
- Original `user.js` + `Softfox.js` performance tuning (many values since re-tiered to Balanced in v157).
