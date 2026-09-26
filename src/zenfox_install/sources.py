"""Download + verify sources — stdlib only (urllib/zipfile/hashlib).

All network input treated as untrusted: https/http only, no credentials in
URL, SHA256 required, zip-slip guarded, allowlist enforced.
"""
import hashlib
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


class SourceError(ValueError):
    pass


ZEN_GITHUB_TAG_URL = (
    "https://github.com/SHIMORA-6600X/ZenFox/releases/download/{tag}/ZenFox-{tag}.zip"
)
ZEN_DEFAULT_TAG = "v157"
ADV_DEFAULT_PAGE = "https://gitlab.com/iahmed_7024-group/advancedfox/-/releases"


def validate_url(url):
    u = urllib.parse.urlparse(url)
    if u.scheme not in ("http", "https"):
        raise SourceError(f"Only http/https allowed: {url!r}")
    if not u.hostname:
        raise SourceError(f"URL has no host: {url!r}")
    if u.username or u.password:
        raise SourceError("Credentials in URL are not allowed")
    return url


def download(url, dest, timeout=60):
    validate_url(url)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "ZenFox-Setup/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1024 * 64)
            if not chunk:
                break
            f.write(chunk)
    return dest


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 64), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_sha256(path, expected):
    actual = sha256_of(Path(path))
    if actual.lower() != expected.lower():
        raise SourceError(f"SHA256 mismatch for {path}: expected {expected}, got {actual}")
    return True


def safe_extract(zip_path, dest_dir, allowlist):
    """Extract only allowlisted top-level names; blocks zip-slip. Returns extracted paths."""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = []
    with zipfile.ZipFile(zip_path) as z:
        for member in z.infolist():
            name = member.filename
            if name not in allowlist:
                continue
            target = (dest_dir / name).resolve()
            if target.parent != dest_dir.resolve():
                continue  # nested/traversal — skip
            with z.open(member) as src, open(target, "wb") as dst:
                dst.write(src.read())
            out.append(target)
    return out


ZEN_ALLOWLIST = {"user.js", "LiteFox.js", "Softfox.js", "policies.json",
                 "README.md", "LICENSE", "CHANGELOG.md", "VERSION"}
ADV_ALLOWLIST = {"user.js"}
