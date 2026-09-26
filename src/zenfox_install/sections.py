"""Section parser/generator for Custom mode — stdlib only, headless-safe.

Splits a preset file on `SECTION:` headers. Generation reuses ORIGINAL block
text so comments/formatting survive; only whole sections are in/out.
"""
import datetime
import re
from pathlib import Path

_HEADER_RE = re.compile(r"SECTION:\s*([A-Za-z0-9 /&'\-]+?)\s*\**\s*$")
_PREF_RE = re.compile(r'^\s*user_pref\(\s*"([^"]+)"\s*,\s*(.+?)\s*\)\s*;(.*)$')
_COMMENTED_RE = re.compile(r'^\s*//\s*user_pref\(')


def parse_sections(text, source_file=""):
    """Return (preamble, sections). Section = dict(file,title,raw,prefs,empty).

    prefs = list of {key, value, comment}. Commented prefs counted, not installed.
    """
    lines = text.splitlines()
    start_idxs = [i for i, l in enumerate(lines) if _HEADER_RE.search(l)]
    preamble = "\n".join(lines[:start_idxs[0]]).strip() if start_idxs else text.strip()
    # raw block starts at the /**** banner above the header when present…
    raw_starts = []
    for idx in start_idxs:
        rs = idx
        if idx > 0 and set(lines[idx - 1].strip()) <= set("/*"):
            rs = idx - 1
        raw_starts.append(rs)
    sections = []
    for n, idx in enumerate(start_idxs):
        # …and ends where the NEXT block starts (never swallow its banner).
        end = raw_starts[n + 1] if n + 1 < len(start_idxs) else len(lines)
        raw = "\n".join(lines[raw_starts[n]:end]).rstrip()
        m = _HEADER_RE.search(lines[idx])
        title = re.sub(r"\s+", " ", m.group(1).strip())
        prefs, commented = [], 0
        for l in lines[idx:end]:
            pm = _PREF_RE.match(l)
            if pm:
                prefs.append({"key": pm.group(1), "value": pm.group(2),
                              "comment": pm.group(3).strip().lstrip("/").strip()})
            elif _COMMENTED_RE.match(l):
                commented += 1
        sections.append({"file": source_file, "title": title, "raw": raw,
                         "prefs": prefs, "commented": commented,
                         "empty": not prefs})
    return preamble, sections


def parse_file(path):
    path = Path(path)
    return parse_sections(path.read_text(encoding="utf-8"), source_file=path.name)


def build_custom_user_js(preamble, sections, enabled):
    """Assemble custom user.js from ORIGINAL blocks of enabled sections."""
    stamp = datetime.datetime.now().strftime("%Y-%m-%d")
    on = [s["title"] for s in sections if s["title"] in enabled]
    header = (f"{preamble}\n\n"
              f"/****************************************************************************\n"
              f" * Custom build ({stamp}): {len(on)}/{len(sections)} sections enabled\n"
              f" * Enabled: {', '.join(on)}\n"
              f" ****************************************************************************/")
    blocks = [s["raw"] for s in sections if s["title"] in enabled]
    return header + "\n\n" + "\n\n".join(blocks) + "\n"


def summarize(section, enabled):
    state = "ON " if enabled else "OFF"
    return f"{state} {section['title']} — {len(section['prefs'])} prefs"


def count_active(sections, enabled):
    return sum(len(s["prefs"]) for s in sections if s["title"] in enabled)
