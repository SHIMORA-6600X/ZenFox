"""Backup + install + revert — stdlib only. Never deletes outside backup dirs."""
import datetime
import shutil
from pathlib import Path


class InstallError(ValueError):
    pass


BACKUP_FILES = ("user.js", "prefs.js", "userChrome.css", "userContent.css",
                "LiteFox.js", "Softfox.js")


def backup_profile(profile_dir):
    profile_dir = Path(profile_dir)
    if not profile_dir.is_dir():
        raise InstallError(f"Profile dir not found: {profile_dir}")
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = profile_dir / f"zenfox-backup-{stamp}"
    backup.mkdir(parents=False, exist_ok=False)
    copied = []
    for name in BACKUP_FILES:
        src = profile_dir / name
        if src.is_file():
            shutil.copy2(src, backup / name)
            copied.append(name)
    (backup / "manifest.txt").write_text(
        f"profile={profile_dir}\nstamp={stamp}\nfiles={','.join(copied)}\n"
    )
    return backup


def revert_backup(profile_dir, backup_dir):
    profile_dir = Path(profile_dir)
    backup_dir = Path(backup_dir)
    if not backup_dir.is_dir() or backup_dir.parent != profile_dir:
        raise InstallError(f"Refusing revert: {backup_dir} is not a direct backup of {profile_dir}")
    manifest = backup_dir / "manifest.txt"
    if not manifest.is_file():
        raise InstallError("Refusing revert: manifest.txt missing")
    for name in BACKUP_FILES:
        src = backup_dir / name
        if src.is_file():
            shutil.copy2(src, profile_dir / name)
    # Installer-managed files that did NOT exist pre-install must go,
    # otherwise revert leaves the profile dirty (fresh-profile case).
    for name in ("user.js", "LiteFox.js", "Softfox.js"):
        if not (backup_dir / name).is_file():
            try:
                (profile_dir / name).unlink()
            except FileNotFoundError:
                pass
    return True


def install_files(src_dir, profile_dir, files):
    src_dir, profile_dir = Path(src_dir), Path(profile_dir)
    if not profile_dir.is_dir():
        raise InstallError(f"Profile dir not found: {profile_dir}")
    if not src_dir.is_dir():
        raise InstallError(f"Source dir not found: {src_dir}")
    done = []
    for name in files:
        if "/" in name or "\\" in name or name.startswith("."):
            raise InstallError(f"Refusing unsafe filename: {name!r}")
        src = src_dir / name
        if not src.is_file():
            raise InstallError(f"Missing source file: {src}")
        shutil.copy2(src, profile_dir / name)
        done.append(name)
    return done


def firefox_lock_present(profile_dir):
    """True if Firefox likely open (lock symlink / lock file / parent.lock)."""
    profile_dir = Path(profile_dir)
    for name in ("lock", ".parentlock", "parent.lock"):
        if (profile_dir / name).exists():
            return True
    return False
