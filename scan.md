# ZenFox — Full Project Scan Report

**Date:** 2026-09-25 (UTC)
**Scope:** `user.js`, `LiteFox.js`, `Softfox.js`, `policies.json`, `README.md`, `LICENSE`, `docs/index.html`, git history
**Method:** static review + `node --check`, duplicate-pref analysis, dead-pref heuristic, JSON validation, docs-vs-code consistency, security/privacy/performance review
**Verdict:** ❌ **Not release-ready as-is — main artifact is broken.** Fix P0 first.

---

## 0. TL;DR + Rate

| Category | Score (/10) | Comment |
|---|---|---|
| Correctness / Functionality | **3/10** | `user.js:14` fatal `SyntaxError`, `LiteFox.js:47` missing `;`, `Softfox.js` self-contradictory |
| Performance engineering | **6/10** | Some valid cache/network/GPU tuning, but many placebo/legacy/aggressive values |
| Security | **5/10** | Fullscreen warning disabled, huge connection/cache inflation, no validation |
| Privacy / Debloat | **7/10** | `LiteFox.js` is the best part; `policies.json` is sane but opinionated |
| Code quality / Maintainability | **4/10** | Version drift, dead prefs, duplication, no lint/CI/tests |
| Documentation | **5/10** | README thin + broken link; site polished but out-of-sync with code |
| Website (`docs/index.html`) | **8/10** | Modern, accessible, performant static page; content drift only issue |
| Repo hygiene / Release | **3/10** | No `.gitignore`, no CI, no packaging script, noisy history, source-vs-zip confusion |
| **Overall** | **5.1/10 — Grade D+ / C-** | **Usable ideas, broken packaging. Fix syntax + Softfox logic + versioning before recommending to users.** |

> Rating scale: 9-10 excellent, 7-8 good, 5-6 mediocre, 3-4 poor, 0-2 broken/dangerous.

---

## 1. Inventory

```
LICENSE        21 lines  MIT, (c) 2026 SHIMORA — OK
README.md      61 lines  install + features + thanks — thin
user.js       208 lines  78x user_pref — MAIN PRESET (ZenFox perf) — BROKEN
LiteFox.js    359 lines  114x user_pref (113 unique) — Debloat/UI — best file
Softfox.js     82 lines   38x user_pref (14 unique) — Smooth-scroll — LOGIC BUG
policies.json  89 lines  valid JSON, 17 policy keys — enterprise policy
docs/index.html 1496 lines single-file site (ZenFox + AdvancedFox marketing)
.git           main only, ~89 commits SHIMORA + 1 senwix, no tags/releases automation visible
```

No `.gitignore`, no `package.json`, no CI (`.github/`), no tests, no build/pack script for `ZenFox.zip`.

Pref counts (regex `user_pref("...")`):

- `user.js`: 78 prefs, 78 unique — good (no dup), 1 fatal syntax error.
- `LiteFox.js`: 114 prefs, 113 unique — 1 duplicate.
- `Softfox.js`: 38 prefs, **14 unique** — 13 keys repeated 2-5x (all options active at once).

---

## 2. P0 — Critical (must fix before any release)

### P0-1 — `user.js:14` stray `/` breaks entire file — SEVERITY: BLOCKER
```js
// user.js:12-14
 * SECTION: GENERAL ...
****************************************************************************/
/
 // PREF: initial paint delay
```
`node --check user.js`:
```
SyntaxError: Invalid regular expression: missing /
```
**Impact:** Firefox `user.js` is executed as JS on startup. A syntax error aborts parsing — users get **zero** of the 78 tweaks, with no error UI. This is the file README tells users to download.
**Fix:** delete line 14 (`/`). Add CI: `node --check *.js` + `python -m json.tool policies.json`.

### P0-2 — `Softfox.js` enables all 5 mutually-exclusive scroll profiles at once
Header says (line 11): `Use only one option at a time! Reset prefs if you decide to use different option.`
Reality: all 5 `OPTION:` blocks are uncommented, so effective values = **last write wins**:
- `apz.overscroll.enabled` x4, `general.smoothScroll` x4, `msdPhysics.enabled` x5, `delta_multiplier_y` x4 (280 → 320 → 210 → 330, final 330 wins), `currentVelocityWeighting` 0.15 → 0.15 → 1 (final 1 wins), etc.
First 3 blocks are dead code. Users cannot pick "Sharpen" vs "Zen" vs "Natural V3" without hand-editing.
**Fix:** keep ONE default active, comment out other 4 with clear `// [PICK ONE]` header, or split into `Softfox-Sharp.js`, `Softfox-Zen.js`, etc. Document reset procedure.

### P0-3 — No releasable artifact matches docs
README + site say: *"Don't download source, download `ZenFox.zip` from Releases"* but repo has **no script to build that zip**, no manifest of what goes in it (`user.js`? + `LiteFox.js`? + `Softfox.js`? + `policies.json`?). Users copying raw `user.js` from main get the broken file above.
**Fix:** add `build.sh` / GH Action that lints + zips versioned `ZenFox-<ver>.zip` with README + LICENSE + chosen `user.js`, and document exact contents.

---

## 3. P1 — Major

### P1-1 — `LiteFox.js:47` missing semicolon
```js
user_pref("layout.css.prefers-color-scheme.content-override", 0)
```
Passes `node --check` via ASI, but inconsistent with other 113 lines + risky if minified/concatenated into release zip. Fix: add `;`.

### P1-2 — Version / URL drift (rename NitroFox → ZenFox incomplete)
- `user.js` header: `version: 152`, url `.../ZenFox` — OK but stale.
- `LiteFox.js`: `version: 156` — 4 versions ahead, no changelog explaining delta.
- `Softfox.js:8`: `url: https://github.com/SHIMORA-6600X/NitroFox` — **old name**.
- `README.md:60`: license link `.../NitroFox/blob/main/LICENSE` — **404 after rename** (should be `.../ZenFox/blob/main/LICENSE`).
- `docs/index.html` advertises `AdvancedFox` (GitLab) that **does not exist in this repo** — cross-repo confusion.
**Fix:** single `VERSION` file or header generator, global find-replace NitroFox → ZenFox, changelog.

### P1-3 — Duplicate pref in `LiteFox.js`
`browser.urlbar.suggest.engines = true` set at line 130 **and** line 163 (same value, harmless but sloppy — suggests copy-paste without dedup). Add duplicate-pref lint.

### P1-4 — Docs code samples do not match shipped code
`docs/index.html` shows:
```js
user_pref("network.http.max-connections", 900);
user_pref("network.http.pipelining", true);
```
Shipped `user.js:167` uses `1800`, and `pipelining` was **removed from Firefox years ago** (dead pref). Same for `browser.cache.disk.enable`, `toolkit.telemetry.enabled`, `network.trr.mode` samples — none match actual files. Marketing claims `60+ tweaks` while actual total is ~230 (78+114+38) or 78 for core — pick one counting method and keep in sync.

### P1-5 — Aggressive / risky perf values with no guardrails
`user.js`:
- `network.http.max-connections 1800` (default 900), `max-persistent-connections-per-server 10` (default 6), `network.http.pacing.requests.enabled false` + burst 20 — faster on ideal networks, but **server-unfriendly, triggers rate-limits, more fingerprintable**. No per-profile (4GB vs 32GB) guidance except one comment.
- `browser.cache.disk.capacity 1024000` (1 GB, 4x default), `media.memory_caches_combined_limit_kb 1048576` (1 GB), `media.cache_readahead_limit 3600` (1 hr readahead, default 60s) + `resume_threshold 1800` — wastes bandwidth/RAM on metered connections, stalls on low-disk devices.
- `browser.low_commit_space_threshold_mb 3276` hardcoded for 4 GB (comment lists 8/16/32/64 GB values but no script to pick) — wrong on most machines.
- `gfx.webrender.all true` + `compositor.force-enabled true` + `precache-shaders true` (longer startup) — breaks on old GPUs / VMs; no fallback note (software WR lines are commented out).
- `javascript.options.baselinejit.threshold 50` (default 100) — faster warmup, higher CPU; no benchmark cited.
- `dom.storage.default_quota 20480` (4x), `network.dnsCacheExpiration 3600` (60x default, stale DNS + captive-portal issues), `network.ssl_tokens_cache_capacity 8192` (TLS resumption tracking surface).

`LiteFox.js`:
- `full-screen-api.warning.timeout 0` + `warning.delay -1` — **removes anti-spoofing delay**. Comment admits *"Adjust to 1250 if you have security concerns"* — default should be safe, opt-in to unsafe.
- `browser.download.useDownloadDir false` (prompt every download) + `always_ask_before_handling_new_types true` — secure but annoying; should be called out as opinionated.
- Disables `history/bookmark/openpage` URL-bar suggestions + `topsites` + `autofill` — big usability loss for "speed" gain; needs user warning.

**Fix:** tier presets (Low-end / Balanced / High-end), document trade-offs, link `about:config` reverts, provide `uninstall/reset` instructions (delete `user.js` + `prefs.js` edits persist — currently undocumented!).

### P1-6 — Legacy / removed prefs shipped as active
`user.js` still sets (verified by string match):
`content.notify.ontimer/interval`, `content.max.tokenizing.time`, `content.interrupt.parsing`, `content.switch.threshold`, `browser.cache.disk.smart_size.enabled`, `nglayout.initialpaint.delay_in_oopif`, `javascript.options.mem.high_water_mark`, `browser.sessionstore.max_entries`, `image.mem.max_decoded_image_kb`, plus `LiteFox.js: extensions.pocket.*` (Pocket removed from modern FF). Dead prefs = false promise + harder maintenance. Audit against `about:config` on ESR + Beta + Nightly each release, or import from BetterFox/Arkenfox upstream with attribution.

### P1-7 — `policies.json` opinionated / stale bits
Valid JSON — good. Issues:
- `WebsiteFilter.Block: ["https://localhost/*"]` — breaks local dev (`http://localhost`, `127.0.0.1`, dev servers). Likely copy-paste error; remove or document.
- `DNSOverHTTPS: {Enabled:false, ProviderURL:""}` — dead config; either configure real DoH or drop key.
- `AppAutoUpdate:true` + `ManualAppUpdateOnly:false` + comments — redundant; pick one.
- `Extensions.Install: [uBlock Origin]` — forces install (good intent, but no consent note + pins `latest` without hash).
- `SearchEngines.Default: DuckDuckGo` + `Add: [DuckDuckGo Lite, SearXNG(searx.be), MetaGer, StartPage]` — `searx.be` reliability questionable; huge base64 `IconURL`s bloat file to 21 KB; `Remove: [Amazon, eBay, Perplexity]` is opinionated.
- `NoDefaultBookmarks:true`, `DisableFirefoxStudies/Telemetry:true` — fine, but should be listed in README feature matrix.

---

## 4. P2 — Minor / Quality

- **Style:** inconsistent indent (`LiteFox.js:20-22` extra spaces, `user.js:69-70`), mixed `// PREF:` / `// [SETTING]` / `// [NOTE]` formats, typo `Uneccesery`, `userChome` (should be `userChrome`), `licence` vs `license`, `SHIMORA` spacing.
- **Comments:** good intent (defaults + FF version gates like `[FF118+]`), but many `[DEFAULT]` tags are wrong (value differs from default — e.g. `browser.cache.disk.capacity`). Either verify or drop tag.
- **README:** 61 lines, no version table, no file matrix (what is Lite vs Soft vs user?), no backup/restore warning beyond one line, no Firefox version support range (115 ESR? 140+?), no benchmark, Discord/Telegram badges but no contribution guide.
- **LICENSE:** MIT OK, year 2026 (future-dated — use 2025-2026 or auto).
- **Git:** history is `Update README.md` x N, `Update index.html` x N — no conventional commits, no tags, no releases notes. 89 commits by SHIMORA, 1 by senwix — thank contributors in README? (iAHMED/Kenjaku mentioned but not in git).
- **Missing files:** `.gitignore`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (optional), `checksums.txt` for releases.

---

## 5. Security Review (summary)

| Finding | Severity | Location |
|---|---|---|
| Fullscreen spoofing guard disabled | **High** | `LiteFox.js:100-101` |
| No integrity / no signature for `ZenFox.zip` | Medium | repo-wide |
| Aggressive network (1800 conns, pacing off) → DoS-like / IP ban risk | Medium | `user.js:167-179` |
| 1-hr media readahead + 1 GB caches → disk/RAM exhaustion on shared machines | Medium | `user.js:95-150` |
| TLS token cache 8192 → resumption tracking | Low | `user.js:189` |
| `policies.json` blocks localhost, forces extensions | Low | `policies.json:29-42` |
| Site `docs/index.html` uses external Google Fonts without SRI, `target=_blank` correctly uses `rel=noopener` — OK | Info | `docs/index.html:9-11` |

No malware, no exfiltration, no obfuscation — project is benign config. Risk is **misconfiguration**, not malice.

---

## 6. Performance Reality Check

Claimed: *"Faster page loads, optimized cache, lightweight, Chrome-like feel, smooth on YouTube/Netflix."*

- **Plausibly real:** larger disk/memory cache helps repeat visits; WebRender+Canvas accel helps on discrete GPUs; reduced sessionstore undo (25→10) lowers I/O; DNS cache 1600 entries helps multi-tab.
- **Placebo / negligible:** `content.notify.*` (legacy), `nglayout.initialpaint.delay 250→5ms` (sub-frame on modern HW), font Skia cache 5→20 MB (Chrome parity claim unverified), `network.buffer.cache` micro-tuning.
- **Regressions possible:** `precache-shaders` slows cold start; 1-hr readahead wastes bandwidth; JIT threshold 50 increases CPU; `low_commit_space_threshold_mb` wrong value causes premature tab unload; forced compositor on weak iGPU causes jank.
- **Missing proof:** no `about:profiling`, no `Speedometer`, no cold/warm load numbers, no A/B vs stock Firefox. Add `docs/benchmarks.md` with hardware matrix before claiming "fastest".

Recommendation: split into `Balanced` (safe) vs `Max` (aggressive) and measure.

---

## 7. Website (`docs/index.html`) — the strongest asset

- **Pros:** single-file, no build step, dark/light themes, `prefers-reduced-motion`, responsive, `content-visibility`, passive listeners, rAF-throttled tilt/spotlight, correct `rel=noopener`, theme-color sync, offline-friendly (except fonts).
- **Cons:** content drift (see P1-4), `AdvancedFox` GitLab links unverifiable from this repo, stats (`60+ tweaks`, `100% open source`) unmeasured, Google Fonts no `display=swap` fallback if offline (has `display=swap` — OK, but no self-host), FPS meter on `D` key hijacks typing (should require modifier), preloader 900ms minimum delays FCP.
- **Score 8/10** — keep design, fix copy + add version badge auto-injected from git tag.

---

## 8. Action Plan (ordered)

1. **[P0] Fix `user.js:14`** — delete stray `/`, run `node --check`.
2. **[P0] Fix `Softfox.js`** — enable ONE scroll profile, comment others; test on 60/120/144 Hz.
3. **[P0] Define release** — `build.sh` → `ZenFox-<tag>.zip` (`user.js`+`LiteFox.js`+`Softfox.js`+`policies.json`+README+LICENSE+checksums); GH Release workflow.
4. **[P1] Sync versions/URLs** — bump all to same version, fix NitroFox links, add `CHANGELOG.md`.
5. **[P1] Audit prefs** — remove dead Pocket/`content.*`/pipelining prefs; verify each `[DEFAULT]` claim on FF 128 ESR + latest stable.
6. **[P1] Harden defaults** — restore fullscreen warning (`1250/500`), make aggressive network/cache opt-in `Max` profile.
7. **[P1] Fix `policies.json`** — drop localhost block or scope correctly, configure or remove DoH stub, document forced uBO.
8. **[P2] Hygiene** — `.gitignore`, CI lint (`node --check` + `jq empty policies.json` + duplicate-pref check), conventional commits, Firefox support matrix in README, uninstall instructions (critical: `user.js` prefs persist in `prefs.js` after deletion — must document `about:support → Refresh`).
9. **[P2] Benchmarks** — publish Speedometer / cold-start / YouTube 4K numbers before marketing claims.
10. **[P2] Docs** — file matrix table (user vs Lite vs Soft vs policies), screenshots, FAQ (revert, ESR, Flatpak paths).

Quick lint you can run now:
```bash
node --check user.js && node --check LiteFox.js && node --check Softfox.js
python3 -m json.tool policies.json > /dev/null && echo "policies OK"
grep -c 'user_pref' *.js
# duplicate check
python3 -c "import re,collections; [print(f, [k for k,v in collections.Counter(re.findall(r'user_pref\(\s*\"([^\"]+)\"', open(f).read())).items() if v>1]) for f in ['user.js','LiteFox.js','Softfox.js']]"
```

---

## 9. Detailed Findings Table

| ID | File:Line | Issue | Severity |
|---|---|---|---|
| F-01 | `user.js:14` | Stray `/` → `SyntaxError`, file unusable | P0 Blocker |
| F-02 | `Softfox.js:17-82` | 5 exclusive options all active, 13 keys dup | P0 Blocker |
| F-03 | `LiteFox.js:47` | Missing `;` | P1 |
| F-04 | `LiteFox.js:130,163` | `suggest.engines` duplicated | P1 |
| F-05 | `Softfox.js:8`, `README:60` | Stale `NitroFox` URLs | P1 |
| F-06 | `user.js:1-10` vs `LiteFox:1-8` | Version 152 vs 156, no changelog | P1 |
| F-07 | `user.js:28-33,95,128,159` | Legacy `content.*`, `smart_size`, `high_water_mark`, `max_entries`, `max_decoded_image_kb` | P1 |
| F-08 | `LiteFox.js:248-252` | Dead `extensions.pocket.*` | P1 |
| F-09 | `docs/index.html:915-917` | Sample uses removed `pipelining:true`, wrong `max-connections` | P1 |
| F-10 | `user.js:167-182` | 1800 conns, pacing off, 1-hr DNS cache | P1 |
| F-11 | `user.js:95-150` | 1 GB disk + 1 GB media + 1-hr readahead | P1 |
| F-12 | `LiteFox.js:100-101` | Fullscreen warning disabled | P1 Security |
| F-13 | `policies.json:29-33` | Blocks `localhost/*` | P1 |
| F-14 | `policies.json:12-16` | Empty DoH stub | P2 |
| F-15 | repo root | No `.gitignore`, CI, tests, build script | P1 Hygiene |
| F-16 | `README.md` | No file matrix, support range, uninstall | P2 |
| F-17 | `docs/index.html:1473` | FPS toggle on bare `D` key | P2 UX |

---

## 10. Final Rate Justification

**5.1/10 (D+/C-).** The project has genuine value — `LiteFox.js` debloat is coherent, `docs/index.html` is well-engineered, `policies.json` is valid — but the flagship `user.js` **does not parse**, `Softfox.js` contradicts its own instructions, and aggressive values ship without benchmarks or safe defaults. Fix the three P0s + version sync and this becomes a solid 7+. Until then, do not distribute `ZenFox.zip` built from `main`.

*Generated by local static scan. Re-run after fixes; add `about:support` + `about:profiling` validation on at least 2 machines (Windows/Linux, 8 GB / 16 GB RAM, 60 Hz / 120 Hz) before next release.*
