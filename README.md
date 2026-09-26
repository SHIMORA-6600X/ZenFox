## ZenFox 

<p align="center">
  <a href="https://discord.gg/bQxe2dkgMW"><img src="https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=blue" alt="Discord"></a>
  <a href="https://t.me/shimora_projects"><img src="https://img.shields.io/badge/Telegram-Join-26A5E4?logo=telegram&logoColor=sky" alt="Join Telegram"></a>
</p>

Custom `user.js` presets that make Firefox faster and calmer. See `CHANGELOG.md` (current: **v157 Balanced**).

[about:config](https://support.mozilla.org/en-US/kb/about-config-editor-firefox) tweaks for [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/).
Support range: ** _Firefox 115 ESR_ + ** (Beta/Nightly may need adjustments; see comments with `[FFxxx+]`).

#### Files (pick what you need)

| File | Purpose | Prefs | Default |
|------|---------|-------|---------|
| `user.js` | Perf core: network, cache, rendering, JS, media, tab unload | ~70 active | Balanced safe — use as-is |
| `LiteFox.js` | Debloat/UI: AI off, translations off, sponsored content off, sane tab/download behavior | ~108 active | Use as-is; fullscreen warning kept safe |
| `Softfox.js` | Smooth scrolling — **[PICK ONE]** profile | 11 active (ZEN) | ZEN SMOOTH active; uncomment only one OPTION |
| `policies.json` | Enterprise policy: telemetry off, uBlock install, search defaults | — | Optional; forces uBlock on first run |
| `docs/index.html` | Project site | — | — |

> `Softfox.js` rule: uncomment **only one** `OPTION:` block. To switch: close Firefox, delete related lines from `prefs.js` (or `about:support > Refresh`), then apply the new option.

#### 📥 _Installation_

> ⚠️ Back up your profile first. `user.js` values persist in `prefs.js` even after you delete `user.js`.

1. _Create a backup profile_ (`about:profiles > Back up` or copy the folder).
2. _Download `ZenFox-v157.zip` from Releases_ (not the `Source code` archive). Zip contains: `user.js`, `LiteFox.js`, `Softfox.js`, `policies.json`, `README.md`, `LICENSE`, `CHANGELOG.md`, `checksums.txt`.
3. _Review overrides_ — search for `Max opt-in` and `[REMOVED v157]` to see aggressive/legacy options.
4. _Open `about:profiles`_, click **Open Folder** on Root Directory for the target profile.
5. _Copy `user.js` (and optionally `LiteFox.js`/`Softfox.js` merged or as separate test runs) into the folder._ `policies.json` goes to Firefox install `distribution/` folder (admin), not the profile.
6. _Restart Firefox._

Validate: `node --check user.js` should pass; run `tools/lint.sh` before reporting issues.

#### ↩️ Uninstall / Revert

Deleting `user.js` does **not** revert applied prefs. Either:
- Restore your backup profile folder, or
- `about:support > Refresh Firefox`, or
- `about:config` → reset each `user_pref` key manually.

#### ✨ _Features_

• ⚡️ _Faster Page Loads – Balanced network/rendering (pacing on, 900 connections, sane DNS cache)_

• 🛠 _Optimized Cache – 512MB disk + 512MB media defaults; repeat visits faster without 1GB bloat_

• 🔋 _Lightweight – Session restore lazy, 10 undo tabs, tab unload on low memory_

• 🔌 _Compatibility – WebRender + Canvas accel with fallback notes for old GPUs/VMs_

• 🪄 _Smooth – One active scroll profile (ZEN), 60/90/120Hz alternatives commented_

• 🛠 _Debloat (LiteFox) – AI/chatbot/translations/sponsored stories off, Pocket remnants removed_

#### 📊 Benchmarks

No numbers yet — see `docs/benchmarks.md` for the method (Speedometer, cold start, YouTube 4K). Claims before that are anecdotal. Contributions with hardware + before/after numbers welcome.

#### 🛠 Setup script (any Firefox, any user)

**No terminal? Double-click `setup.sh`** (Linux) — it opens a window automatically:
tkinter GUI if `python3-tk` is present, else system dialogs (zenity), else a
terminal as last resort. `ZenFox-Setup.desktop` adds a clickable app icon
(copy it to `~/.local/share/applications` or your Desktop, then Allow Launching).
Windows: double-click `setup.bat` (no console window via `pythonw`).

**Windows .exe (no Python needed):** download `ZenFox-Setup-Windows.exe` from
GitHub Releases (or the `release-windows-exe` workflow Artifacts) — double-click
opens the setup window directly. Built automatically on Windows CI from this repo
(`python tools/build_installer.py --windowed`); PyInstaller can't cross-compile,
so the exe is never built on Linux/macOS.

Needs: `python3` only. The windowed UI works out of the box via the bundled
Tk runtime (`thirdparty/tk`, Linux x86_64, ~7 MB, zero installs); a system
`python3-tk` is used when present and preferred. The one-click system install
offer in `setup.sh` remains as a fallback.

Stdlib-only Python, interactive picker with ZenFox vs AdvancedFox info:

```bash
python3 setup.py                        # interactive: pick preset + profile, backup + install
python3 setup.py --list-profiles        # list detected profiles (Win/Linux/macOS + Flatpak/Snap)
python3 setup.py --preset zenfox --profile default --with-lite --with-soft
python3 setup.py --preset advancedfox --profile work --adv-url <...>.zip --adv-sha256 <hex>
python3 setup.py --dry-run               # Zen vs Advanced diff, writes nothing
python3 setup.py --revert <profile>/zenfox-backup-YYYYMMDD-HHMMSS
```

No profile yet (fresh Firefox)? The GUI offers **Create new…**, the terminal asks,
or run non-interactively: `python3 setup.py --preset zenfox --create-profile work --yes`.

**Offline by default:** both presets install from local files — no download needed.
AdvancedFox 1.0.0 is vendored in `vendor/advancedfox/` (per-OS weak/medium/strong,
see `VENDOR.md`); pick the level in the GUI or `--adv-level`. Live upstream zips
remain available via `--adv-url <...>.zip --adv-sha256 <hex>`.

**Custom mode:** GUI `Custom` tab (or `--sections`/`--lite-sections`, see
`python3 setup.py --list-sections`) installs only the `SECTION:` blocks you tick —
left list on/off, center preview, right change log, `apply changes` writes the file.

- ZenFox installs from local repo files (pinned v157); AdvancedFox downloads at runtime (hash-pinned `.zip` required).
- Backup first (`zenfox-backup-*` + manifest), warns if Firefox is open, `--policies` needs admin (copies `policies.json` to Firefox `distribution/`).
- Close Firefox before installing. Tests: `python3 -m unittest discover -s tests`.
- Frozen builds: `bash tools/build_installer.sh` (needs `pip install pyinstaller`) → `dist/ZenFox-Setup-<OS>`.

#### 🛡 Security notes

- Fullscreen warning kept at safe `1250/500`. Setting `0/-1` disables anti-spoofing — opt-in only.
- `policies.json` no longer blocks `localhost/*`. Forced uBlock install is by design when you use the policy file.

|*It's important to read this* |  *Files*    | _Note_    |
|-------|-----|-------|
| *Don't Download it* |  *Source code* ❎ | *that's the source code on main page not in Releases* |
|  *Download it*      |  *ZenFox.zip* ✔️| *Built by `tools/build.sh`, includes checksums*  |

#### 💎 _SUPPORT_

_if You like MY project please leave a Star_ ⭐

#### 🌹 _SPECIAL THANKS FOR_
[iAHMED](https://github.com/A7md70242602GH)
_Giving Some Ideas & Testing The Project's_

[Kenjaku](https://github.com/kenjaku-dev)
_For Helping Me To Making a Website For My Project's_

#### 🧾 _LICENSE_
_This project is under_ [MIT](https://github.com/SHIMORA-6600X/ZenFox/blob/main/LICENSE) _License_
