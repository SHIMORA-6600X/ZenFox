#!/usr/bin/env bash
# ZenFox build — produces versioned ZenFox-<ver>.zip + checksums.
# Contents: presets + vendor/advancedfox (offline) + installer + docs.
set -euo pipefail
cd "$(dirname "$0")/.."

./tools/lint.sh

VER=$(cat VERSION | tr -d ' \n')
OUT="ZenFox-v${VER}.zip"
rm -f "$OUT" checksums.txt
python3 - "$OUT" <<'PY'
import sys, zipfile, pathlib
out = sys.argv[1]
top = ["user.js", "LiteFox.js", "Softfox.js", "policies.json", "README.md",
       "LICENSE", "CHANGELOG.md", "VERSION", "setup.py", "setup.sh", "setup.bat",
       "ZenFox-Setup.desktop"]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in top:
        z.write(f, f)
    for p in sorted(pathlib.Path("vendor/advancedfox").glob("*")):
        z.write(p, f"vendor/advancedfox/{p.name}")
    for p in sorted(pathlib.Path("src/zenfox_install").glob("*.py")):
        z.write(p, f"src/zenfox_install/{p.name}")
print(f"Built {out} via python zipfile")
PY
python3 - <<'PY'
import hashlib, pathlib
files = [f"ZenFox-v{open('VERSION').read().strip()}.zip", "user.js", "LiteFox.js", "Softfox.js", "policies.json"]
with open("checksums.txt", "w") as out:
    for f in files:
        h = hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
        out.write(f"{h}  {f}\n")
PY
echo "Built $OUT"
cat checksums.txt
echo "Zip contents:"
python3 - "$OUT" <<'PY'
import sys, zipfile
with zipfile.ZipFile(sys.argv[1]) as z:
    for i in z.infolist():
        print(f"{i.file_size:>8}  {i.filename}")
PY
