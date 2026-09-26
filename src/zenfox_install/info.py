"""Preset metadata + dry-run helpers — stdlib only.

Both presets install OFFLINE from local files. AdvancedFox is vendored
(see vendor/advancedfox/VENDOR.md); --adv-url/--zen-url overrides still allow
hash-pinned live downloads. sources.py does the fetching.
"""
from pathlib import Path
import re

ZEN_VERSION_FILE = "VERSION"
ADV_DEFAULT_URL = (
    "https://gitlab.com/iahmed_7024-group/advancedfox/-/releases"
)
ADV_VENDOR_TAG = "AdvancedFox_1.0.0-release"
ADV_LEVELS = ("weak", "medium", "strong")


def adv_vendor_file(repo_root, os_name="linux", level="medium"):
    """Local vendored AdvancedFox user.js. macOS has no upstream variant → linux."""
    os_key = "windows" if os_name == "windows" else "linux"
    if level not in ADV_LEVELS:
        raise ValueError(f"Unknown AdvancedFox level: {level!r} (weak|medium|strong)")
    return Path(repo_root) / "vendor" / "advancedfox" / f"{os_key}-{level}.js"


def adv_vendor_policies(repo_root, level="medium"):
    if level not in ADV_LEVELS:
        raise ValueError(f"Unknown AdvancedFox level: {level!r} (weak|medium|strong)")
    return Path(repo_root) / "vendor" / "advancedfox" / f"policies-{level}.json"

PRESETS = {
    "zenfox": {
        "name": "ZenFox v157 Balanced (this repo)",
        "version": "v157",
        "source": "local repo files, offline (pinned v157)",
        "prefs": "~63 active (user.js core)",
        "best_for": "everyday speed, old laptops, safe defaults",
        "risk": "low — Balanced defaults, reversible via backup",
        "files": ["user.js", "LiteFox.js (opt-in)", "Softfox.js ZEN (opt-in)"],
    },
    "advancedfox": {
        "name": "AdvancedFox 1.0.0 (vendored, offline)",
        "version": "1.0.0 (vendored 2026-09-25)",
        "source": "vendor/advancedfox/ (upstream GitLab release, per-OS medium default)",
        "prefs": "~35 active privacy/hardening prefs (Medium level, per-OS)",
        "best_for": "power users wanting hardening",
        "risk": "medium — strict settings can break sites (see upstream notes); use Compare first",
        "files": ["user.js (vendored per-OS weak|medium|strong)"],
    },
}


def compare_table():
    rows = [
        ("", "1) ZenFox", "2) AdvancedFox"),
        ("Source", "this repo (pinned v157)", "vendored 1.0.0, offline"),
        ("Contents", PRESETS["zenfox"]["prefs"], PRESETS["advancedfox"]["prefs"]),
        ("Best for", PRESETS["zenfox"]["best_for"], PRESETS["advancedfox"]["best_for"]),
        ("Risk", PRESETS["zenfox"]["risk"], PRESETS["advancedfox"]["risk"]),
    ]
    widths = [max(len(r[i]) for r in rows) for i in range(3)]
    lines = []
    for r in rows:
        lines.append(" | ".join(c.ljust(w) for c, w in zip(r, widths)))
    lines.insert(1, "-+-".join("-" * w for w in widths))
    return "\n".join(lines)


_PREF_RE = re.compile(r'^\s*user_pref\(\s*"([^"]+)"\s*,\s*(.+?)\s*\)\s*;')


def parse_user_prefs(text):
    """Parse ACTIVE user_pref lines only (commented lines ignored)."""
    out = {}
    for line in text.splitlines():
        m = _PREF_RE.match(line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def diff_keys(first, second):
    a, b = set(first), set(second)
    return {
        "only_first": sorted(a - b),
        "only_second": sorted(b - a),
        "both": sorted(a & b),
    }


def format_diff(diff, first_name="zenfox", second_name="advancedfox", limit=30):
    lines = [f"Only in {first_name} ({len(diff['only_first'])}):"]
    lines += [f"  {k}" for k in diff["only_first"][:limit]]
    lines.append(f"Only in {second_name} ({len(diff['only_second'])}):")
    lines += [f"  {k}" for k in diff["only_second"][:limit]]
    lines.append(f"Shared ({len(diff['both'])}) — values may still differ, check manually.")
    return "\n".join(lines)
