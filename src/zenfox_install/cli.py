"""CLI — stable flags (additive only). Interactive picker by default.

  setup.py [--preset zenfox|advancedfox] [--profile NAME|PATH]
           [--with-lite] [--with-soft] [--policies [--firefox-dir DIR]]
           [--revert BACKUP_DIR] [--dry-run] [--list-profiles]
           [--zen-url URL --zen-sha256 HEX] [--zen-tag TAG]
           [--adv-url URL --adv-sha256 HEX] [--yes]
"""
import argparse
import sys
import tempfile
from pathlib import Path

from . import info, install, policies, profiles, sections, sources


def build_parser():
    p = argparse.ArgumentParser(description="ZenFox setup — install presets into any Firefox profile.")
    p.add_argument("--preset", choices=["zenfox", "advancedfox"])
    p.add_argument("--profile", help="Profile name (from profiles.ini) or full path")
    p.add_argument("--create-profile", nargs="?", const="zenfox", metavar="NAME",
                   help="Create a new Firefox profile (default name 'zenfox') and use it")
    p.add_argument("--with-lite", action="store_true", help="Also install LiteFox.js (ZenFox only)")
    p.add_argument("--with-soft", action="store_true", help="Also install Softfox.js (ZenFox only)")
    p.add_argument("--policies", action="store_true", help="Also install policies.json (needs admin)")
    p.add_argument("--firefox-dir", help="Firefox install dir for policies.json")
    p.add_argument("--revert", metavar="BACKUP_DIR", help="Restore a zenfox-backup-* dir and exit")
    p.add_argument("--dry-run", action="store_true", help="Show Zen vs Advanced diff, write nothing")
    p.add_argument("--list-profiles", action="store_true")
    p.add_argument("--list-sections", action="store_true",
                   help="List FILE\\tTITLE\\tN installable sections (for custom mode)")
    p.add_argument("--zen-url", help="Override: download ZenFox zip instead of local files")
    p.add_argument("--zen-sha256", help="Required with --zen-url")
    p.add_argument("--zen-tag", default="v157", help="GitHub release tag for default ZenFox URL")
    p.add_argument("--adv-url", default=info.ADV_DEFAULT_URL,
                   help="Override: download upstream .zip instead of vendored files")
    p.add_argument("--adv-sha256", help="Required when --adv-url points to a .zip")
    p.add_argument("--adv-level", choices=list(info.ADV_LEVELS), default="medium",
                   help="Vendored AdvancedFox level (default: medium)")
    p.add_argument("--sections",
                   help="Custom ZenFox user.js: comma-separated SECTION titles to include (default: all)")
    p.add_argument("--lite-sections",
                   help="Custom LiteFox.js: comma-separated SECTION titles (requires --with-lite)")
    p.add_argument("--yes", action="store_true", help="Skip consent prompt (automation)")
    return p


def _is_tty():
    return sys.stdin.isatty()


def _ask(prompt):
    """input() that survives dead stdin: EOFError -> None (clean abort)."""
    try:
        return input(prompt)
    except EOFError:
        return None


def pick_preset():
    print(info.compare_table())
    print("\n[1] ZenFox  [2] AdvancedFox  [3] Dry-run compare (no install)")
    while True:
        choice = _ask("Pick [1/2/3]: ")
        if choice is None:
            return None
        choice = choice.strip()
        if choice == "1":
            return "zenfox"
        if choice == "2":
            return "advancedfox"
        if choice == "3":
            return "dryrun-compare"


def pick_profile(found):
    if not found:
        print("No profiles found in standard locations.")
        while True:
            sel = _ask("Create a new profile [c], or paste a full profile path: ")
            if sel is None:
                return None
            sel = sel.strip()
            if sel.lower() in ("c", "create", ""):
                created = profiles.create_profile(profiles.choose_creation_root(profiles.data_roots()))
                print(f"Created profile '{created['name']}' at {created['path']}")
                return created["path"]
            cand = Path(sel).expanduser()
            if cand.is_dir():
                return cand
            print("Invalid choice, try again.")
    print("Firefox profiles found:")
    for i, p in enumerate(found):
        mark = " (default)" if p["is_default"] else ""
        print(f"  [{i}] {p['name']}{mark} — {p['path']}")
    print("  [c] Create a new profile")
    while True:
        sel = _ask(f"Pick [0-{len(found) - 1}], [c]reate, or paste a path: ")
        if sel is None:
            return None
        sel = sel.strip()
        if sel.lower() in ("c", "create"):
            created = profiles.create_profile(profiles.choose_creation_root(profiles.data_roots()))
            print(f"Created profile '{created['name']}' at {created['path']}")
            return created["path"]
        if sel.isdigit() and 0 <= int(sel) < len(found):
            return found[int(sel)]["path"]
        cand = Path(sel).expanduser()
        if cand.is_dir():
            return cand
        print("Invalid choice, try again.")


def repo_root():
    # Frozen (PyInstaller onefile): data files live in the bundle temp dir.
    import sys
    frozen_base = getattr(sys, "_MEIPASS", None)
    if frozen_base and (Path(frozen_base) / "user.js").is_file():
        return Path(frozen_base)
    # src/zenfox_install/cli.py -> repo root (or PyInstaller bundle dir)
    here = Path(__file__).resolve()
    for parent in [here.parent.parent.parent, Path.cwd()]:
        if (parent / "user.js").is_file() and (parent / "VERSION").is_file():
            return parent
    return Path.cwd()


def resolve_zen_files(args, tmpdir):
    """Return (src_dir, files). Local repo files by default; download if --zen-url."""
    if args.zen_url:
        if not args.zen_sha256:
            raise sources.SourceError("--zen-url requires --zen-sha256 (hash-pinned downloads only)")
        z = Path(tmpdir) / "zen.zip"
        sources.download(args.zen_url, z)
        sources.verify_sha256(z, args.zen_sha256)
        out = Path(tmpdir) / "zen"
        sources.safe_extract(z, out, sources.ZEN_ALLOWLIST)
        src = out
    else:
        src = repo_root()
    files = ["user.js"]
    if args.with_lite:
        files.append("LiteFox.js")
    if args.with_soft:
        files.append("Softfox.js")
    for f in files:
        if not (src / f).is_file():
            raise sources.SourceError(f"ZenFox source missing: {src / f}")
    return src, files


def _current_os_key():
    import platform
    return {"Windows": "windows", "Darwin": "macos"}.get(platform.system(), "linux")


def resolve_adv_files(args, tmpdir):
    """Vendored offline default; live download only when --adv-url overridden."""
    url = (args.adv_url or info.ADV_DEFAULT_URL).strip()
    if url != info.ADV_DEFAULT_URL:
        if not url.endswith(".zip"):
            raise sources.SourceError(
                f"AdvancedFox --adv-url must point to a release .zip asset.\n"
                f"Release page: {info.ADV_DEFAULT_URL}\n"
                f"Re-run with: --adv-url <...>.zip --adv-sha256 <hex>")
        if not getattr(args, "adv_sha256", None):
            raise sources.SourceError("AdvancedFox .zip requires --adv-sha256")
        z = Path(tmpdir) / "adv.zip"
        sources.download(url, z)
        sources.verify_sha256(z, args.adv_sha256)
        out = Path(tmpdir) / "adv"
        sources.safe_extract(z, out, sources.ADV_ALLOWLIST)
        return out, ["user.js"]
    level = getattr(args, "adv_level", "medium") or "medium"
    src_file = info.adv_vendor_file(repo_root(), _current_os_key(), level)
    if not src_file.is_file():
        raise sources.SourceError(f"Vendored AdvancedFox missing: {src_file}")
    out = Path(tmpdir) / "adv-local"
    out.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(src_file, out / "user.js")
    return out, ["user.js"]


def _parse_section_list(raw, known_titles, what):
    """Comma-separated titles → validated set. None/empty means ALL."""
    if not raw:
        return set(known_titles)
    keep = {t.strip() for t in raw.split(",") if t.strip()}
    unknown = keep - set(known_titles)
    if unknown:
        raise sources.SourceError(
            f"Unknown {what} section(s): {sorted(unknown)}\nKnown: {sorted(known_titles)}")
    return keep


def build_custom_files(repo, user_keep=None, lite_keep=None):
    """Return {filename: content} for Custom mode. lite_keep=None → skip LiteFox.

    Raises SourceError on unknown titles.
    """
    u_pre, u_secs = sections.parse_file(Path(repo) / "user.js")
    u_titles = [s["title"] for s in u_secs]
    files = {"user.js": sections.build_custom_user_js(
        u_pre, u_secs, _parse_section_list(user_keep, u_titles, "user.js"))}
    if lite_keep is not None:
        l_pre, l_secs = sections.parse_file(Path(repo) / "LiteFox.js")
        l_titles = [s["title"] for s in l_secs]
        files["LiteFox.js"] = sections.build_custom_user_js(
            l_pre, l_secs, _parse_section_list(lite_keep, l_titles, "LiteFox.js"))
    return files


def run_dry_run(args):
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        zsrc, _ = resolve_zen_files(type("A", (), {"zen_url": None, "with_lite": False, "with_soft": False})(), tmp)
        zen_keys = info.parse_user_prefs((Path(zsrc) / "user.js").read_text())
        try:
            asrc, _ = resolve_adv_files(args, tmp)
            adv_keys = info.parse_user_prefs((Path(asrc) / "user.js").read_text())
        except sources.SourceError as e:
            print(f"(AdvancedFox not fetched: {e})\nShowing ZenFox keys only.")
            print(f"ZenFox active prefs: {len(zen_keys)}")
            return 0
        diff = info.diff_keys(zen_keys, adv_keys)
        print(info.format_diff(diff))
        return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_profiles:
        found = profiles.list_profiles()
        if not found:
            print("No profiles found.")
        for p in found:
            mark = " (default)" if p["is_default"] else ""
            print(f"{p['name']}{mark} — {p['path']}")
        return 0

    if args.list_sections:
        for fname in ("user.js", "LiteFox.js"):
            _, secs = sections.parse_file(repo_root() / fname)
            for s in secs:
                print(f"{fname}\t{s['title']}\t{len(s['prefs'])}")
        return 0

    # Revert path (no other action)
    if args.revert:
        backup = Path(args.revert)
        profile_dir = backup.parent
        install.revert_backup(profile_dir, backup)
        print(f"Restored backup {backup} into {profile_dir}. Restart Firefox.")
        return 0

    if args.dry_run:
        return run_dry_run(args)

    # Resolve preset
    preset = args.preset
    if not preset:
        if _is_tty() and not args.yes:
            preset = pick_preset()
            if preset is None:
                print("Aborted: no input (stdin closed?). "
                      "Use --preset/--profile/--yes, or --gui.", file=sys.stderr)
                return 1
            if preset == "dryrun-compare":
                return run_dry_run(args)
        else:
            parser.error("--preset is required in non-interactive mode")

    # Resolve profile
    found = profiles.list_profiles()
    if args.create_profile is not None:
        created = profiles.create_profile(
            profiles.choose_creation_root(profiles.data_roots()),
            name=args.create_profile or "zenfox")
        print(f"Created profile '{created['name']}' at {created['path']}")
        profile_dir = created["path"]
    elif args.profile:
        try:
            profile_dir = profiles.resolve_profile(args.profile, found)
        except profiles.ProfileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
    elif _is_tty():
        profile_dir = pick_profile(found)
        if profile_dir is None:
            print("Aborted: no input (stdin closed?). "
                  "Use --preset/--profile/--yes, or --gui.", file=sys.stderr)
            return 1
    else:
        parser.error("--profile is required in non-interactive mode")
    profile_dir = Path(profile_dir)
    if not profile_dir.is_dir():
        print(f"Error: profile dir not found: {profile_dir}", file=sys.stderr)
        return 2

    # Validate custom section lists BEFORE consent/backup (fail fast, no side effects).
    if preset == "zenfox" and (args.sections or args.lite_sections is not None):
        if args.lite_sections is not None and not args.with_lite:
            parser.error("--lite-sections requires --with-lite")
        try:
            _, u_secs = sections.parse_file(repo_root() / "user.js")
            _parse_section_list(args.sections, [s["title"] for s in u_secs], "user.js")
            if args.lite_sections is not None:
                _, l_secs = sections.parse_file(repo_root() / "LiteFox.js")
                _parse_section_list(args.lite_sections, [s["title"] for s in l_secs], "LiteFox.js")
        except sources.SourceError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

    # Consent + info
    if preset == "advancedfox" and (args.with_lite or args.with_soft):
        print("Note: --with-lite/--with-soft are ZenFox-only; ignored for AdvancedFox.")
    if not args.yes and _is_tty():
        print(info.compare_table())
        print(f"\nPreset: {preset}\nProfile: {profile_dir}")
        print("This backs up user.js/prefs.js first. policies.json needs admin (see --policies).")
        if (_ask("Continue? [y/N]: ") or "n").strip().lower() != "y":
            print("Aborted.")
            return 1

    # Firefox-open guard (warn, don't force)
    if install.firefox_lock_present(profile_dir) and not args.yes:
        print("WARNING: Firefox looks open (lock file present). Close it first or prefs.js may be overwritten.")
        if _is_tty() and (_ask("Continue anyway? [y/N]: ") or "n").strip().lower() != "y":
            return 1

    backup = install.backup_profile(profile_dir)
    print(f"Backup: {backup}")

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        if preset == "zenfox":
            if args.sections or args.lite_sections is not None:
                try:
                    custom = build_custom_files(
                        repo_root(), args.sections,
                        args.lite_sections if args.with_lite else None)
                except sources.SourceError as e:
                    print(f"Error: {e}", file=sys.stderr)
                    return 2
                src = Path(tmp) / "custom"
                src.mkdir()
                for name, content in custom.items():
                    (src / name).write_text(content, encoding="utf-8")
                files = list(custom)
                print(f"Custom build: {', '.join(files)}")
            else:
                src, files = resolve_zen_files(args, tmp)
        else:
            if args.sections or args.lite_sections is not None:
                print("Note: --sections/--lite-sections are ZenFox-only; ignored for AdvancedFox.")
            src, files = resolve_adv_files(args, tmp)
        done = install.install_files(src, profile_dir, files)
    print(f"Installed into {profile_dir}: {', '.join(done)}")

    if args.policies:
        if not policies.is_admin():
            print("Skipping policies.json: needs admin rights. Re-run as admin or copy manually.")
        else:
            import platform
            os_name = {"Windows": "windows", "Darwin": "macos"}.get(platform.system(), "linux")
            dests = policies.distribution_dirs(os_name, args.firefox_dir)
            dest = dests[0]
            if preset == "advancedfox":
                level = args.adv_level or "medium"
                src_pol = info.adv_vendor_policies(repo_root(), level)
                print(f"Using vendored AdvancedFox policies ({level}).")
            else:
                src_pol = (repo_root() / "policies.json")
            policies.install_policies(src_pol, dest)
            print(f"policies.json -> {dest}")

    print("Done. Restart Firefox. Revert: setup.py --revert "
          f"{backup}  (or restore your pre-run backup).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
