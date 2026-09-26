#!/usr/bin/env bash
# ZenFox lint — TDD RED guard. Fails on syntax, bad JSON, dup prefs, stale renames.
set -euo pipefail
cd "$(dirname "$0")/.."

FAIL=0

echo "== node --check =="
for f in user.js LiteFox.js Softfox.js; do
  if node --check "$f"; then
    echo "OK $f"
  else
    echo "FAIL $f"; FAIL=1
  fi
done

echo "== policies.json =="
if python3 -m json.tool policies.json > /dev/null; then
  echo "OK policies.json"
else
  echo "FAIL policies.json"; FAIL=1
fi

echo "== duplicate user_pref check =="
python3 - "$@" <<'PY'
import re, collections, sys
active_only = "--active-only" in sys.argv
fail = False
for f in ["user.js", "LiteFox.js", "Softfox.js"]:
    prefs = []
    for line in open(f):
        s = line.strip()
        if not s.startswith("user_pref("):
            continue  # commented lines ignored; use --active-only is default behavior
        m = re.search(r'user_pref\(\s*"([^"]+)"', line)
        if m:
            prefs.append(m.group(1))
    c = collections.Counter(prefs)
    dups = {k: v for k, v in c.items() if v > 1}
    if dups:
        print(f"FAIL {f} duplicates: {dups}")
        fail = True
    else:
        print(f"OK {f} ({len(prefs)} active prefs, {len(set(prefs))} unique)")
sys.exit(1 if fail else 0)
PY
[ $? -eq 0 ] || FAIL=1

echo "== stale NitroFox guard =="
# Exclude lint script itself, history docs, and arrow-notation migration notes.
if grep -rn "NitroFox" --exclude-dir=.git --exclude-dir=.github --exclude=scan.md --exclude=CHANGELOG.md --exclude=lint.sh . | grep -v "NitroFox →" | grep -v "NitroFox," ; then
  echo "FAIL stale NitroFox reference found"; FAIL=1
else
  echo "OK no stale NitroFox"
fi

echo "== version sync =="
VER=$(cat VERSION | tr -d ' \n')
for f in user.js LiteFox.js Softfox.js; do
  if grep -q "version: $VER" "$f"; then
    echo "OK $f version $VER"
  else
    echo "FAIL $f missing version: $VER"; FAIL=1
  fi
done

echo "== vendored AdvancedFox =="
for f in vendor/advancedfox/VENDOR.md vendor/advancedfox/linux-weak.js vendor/advancedfox/linux-medium.js vendor/advancedfox/linux-strong.js vendor/advancedfox/windows-weak.js vendor/advancedfox/windows-medium.js vendor/advancedfox/windows-strong.js vendor/advancedfox/policies-weak.json vendor/advancedfox/policies-medium.json vendor/advancedfox/policies-strong.json; do
  if [ -f "$f" ]; then :; else echo "FAIL missing $f"; FAIL=1; fi
done
for f in vendor/advancedfox/*.js; do
  node --check "$f" || { echo "FAIL $f"; FAIL=1; }
done
python3 -m json.tool vendor/advancedfox/policies-medium.json > /dev/null || { echo "FAIL adv policies json"; FAIL=1; }
grep -q "AdvancedFox_1.0.0-release" vendor/advancedfox/VENDOR.md || { echo "FAIL VENDOR.md tag"; FAIL=1; }
echo "OK vendor/advancedfox (9 files + provenance)"

echo "== bundled Tk runtime =="
for f in thirdparty/tk/README.md thirdparty/tk/licenses/tk-license.terms thirdparty/tk/licenses/license.terms thirdparty/tk/linux-x86_64/libtk8.6.so thirdparty/tk/linux-x86_64/libtcl8.6.so; do
  if [ -f "$f" ]; then :; else echo "FAIL missing $f"; FAIL=1; fi
done
for d in thirdparty/tk/linux-x86_64/tcl8.6 thirdparty/tk/linux-x86_64/tk8.6; do
  if [ -d "$d" ]; then :; else echo "FAIL missing dir $d"; FAIL=1; fi
done
echo "OK thirdparty/tk (libs + scripts + licenses)"

if [ "$FAIL" -ne 0 ]; then
  echo "LINT FAILED"; exit 1
fi
echo "LINT PASSED"
