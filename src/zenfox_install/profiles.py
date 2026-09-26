"""Firefox profile discovery — stdlib only, Win/Linux/macOS + Flatpak/Snap.

Contract (stable):
  data_roots(os_override=None, home_override=None, env_override=None) -> list[Path]
  find_profiles_ini(roots) -> list[Path]  (existing profiles.ini files)
  parse_profiles_ini(ini_path) -> list[dict{name, path, is_default, is_relative}]
  list_profiles(...) -> combined list across roots
  resolve_profile(spec, profiles) -> Path  (raises ProfileNotFoundError)
"""
import configparser
import os
import platform
from pathlib import Path


class ProfileNotFoundError(LookupError):
    pass


def _current_os(os_override=None):
    if os_override:
        return os_override.lower()
    sys = platform.system().lower()
    if sys.startswith("win"):
        return "windows"
    if sys == "darwin":
        return "macos"
    return "linux"


def data_roots(os_override=None, home_override=None, env_override=None):
    """Return candidate Firefox data dirs (may not exist). Order = priority."""
    os_name = _current_os(os_override)
    env = env_override if env_override is not None else os.environ
    home = Path(home_override) if home_override else Path.home()
    if os_name == "windows":
        appdata = Path(env.get("APPDATA", str(home / "AppData/Roaming")))
        local = Path(env.get("LOCALAPPDATA", str(home / "AppData/Local")))
        return [
            appdata / "Mozilla" / "Firefox",
            local / "Mozilla" / "Firefox",
        ]
    if os_name == "macos":
        return [home / "Library" / "Application Support" / "Firefox"]
    # linux + variants
    return [
        home / ".mozilla" / "firefox",
        home / ".var" / "app" / "org.mozilla.firefox" / ".mozilla" / "firefox",  # flatpak
        home / "snap" / "firefox" / "common" / ".mozilla" / "firefox",  # snap
    ]


def find_profiles_ini(roots):
    return [r / "profiles.ini" for r in roots if (r / "profiles.ini").is_file()]


def parse_profiles_ini(ini_path):
    ini_path = Path(ini_path)
    if not ini_path.is_file():
        return []
    cp = configparser.ConfigParser()
    try:
        cp.read(ini_path, encoding="utf-8")
    except (configparser.Error, OSError):
        return []
    out = []
    for section in cp.sections():
        if not section.lower().startswith("profile"):
            continue
        name = cp[section].get("Name", section)
        raw_path = cp[section].get("Path", "")
        if not raw_path:
            continue
        is_rel = cp[section].get("IsRelative", "1") == "1"
        is_default = cp[section].get("Default", "0") == "1"
        path = (ini_path.parent / raw_path) if is_rel else Path(raw_path)
        out.append({"name": name, "path": path, "is_default": is_default,
                    "is_relative": is_rel, "ini": ini_path})
    return out


def list_profiles(os_override=None, home_override=None, env_override=None, roots=None):
    if roots is None:
        roots = data_roots(os_override, home_override, env_override)
    found = []
    for ini in find_profiles_ini(roots):
        found.extend(parse_profiles_ini(ini))
    return found


def resolve_profile(spec, profiles):
    """Match by profile Name or by exact path string. Raises ProfileNotFoundError."""
    for p in profiles:
        if spec == p["name"] or spec == str(p["path"]):
            return p["path"]
    # allow direct existing dir even if not listed
    candidate = Path(spec).expanduser()
    if candidate.is_dir():
        return candidate
    raise ProfileNotFoundError(f"Unknown profile: {spec!r}")


def choose_creation_root(roots):
    """First existing data dir, else the first candidate (created on demand)."""
    for r in roots:
        if Path(r).is_dir():
            return Path(r)
    return Path(roots[0])


def create_profile(root, name="zenfox"):
    """Create a new Firefox profile dir + register it in profiles.ini.

    First-ever profile becomes Default; later ones never steal default.
    Returns dict{name, path, is_default}. Case of existing keys preserved.
    """
    import secrets

    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    ini_path = root / "profiles.ini"

    cp = configparser.ConfigParser()
    cp.optionxform = str  # keep Name/Path/IsRelative/Default casing
    if ini_path.is_file():
        cp.read(ini_path, encoding="utf-8")

    indexes = [int(s[7:]) for s in cp.sections()
               if s.lower().startswith("profile") and s[7:].isdigit()]
    next_index = max(indexes) + 1 if indexes else 0
    has_default = any(cp[s].get("Default", "0") == "1" for s in cp.sections()
                      if s.lower().startswith("profile"))

    dirname = f"{secrets.token_hex(4)}.{name}"
    profile_dir = root / dirname
    profile_dir.mkdir(parents=False, exist_ok=False)

    section = f"Profile{next_index}"
    cp[section] = {"Name": name, "IsRelative": "1", "Path": dirname,
                   "Default": "0" if has_default else "1"}
    if "General" not in cp:
        cp["General"] = {"StartWithLastProfile": "1", "Version": "2"}
    with open(ini_path, "w", encoding="utf-8") as f:
        cp.write(f)

    return {"name": name, "path": profile_dir,
            "is_default": not has_default, "is_relative": True, "ini": ini_path}
