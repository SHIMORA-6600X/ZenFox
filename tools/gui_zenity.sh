#!/usr/bin/env bash
# Zenity fallback UI (Linux without python3-tk). Collects choices with dialogs,
# then drives setup.py CLI underneath — no install logic duplicated here.
set -u
cd "$(dirname "$0")/.."

TITLE="ZenFox Setup"

have() { command -v "$1" >/dev/null 2>&1; }
have zenity || { echo "zenity not found; run: python3 setup.py" >&2; exit 2; }

# --- 1. preset (radiolist shows the info) -------------------------------------
PRESET=$(zenity --list --radiolist --title="$TITLE" --width=620 --height=340 \
  --text="Choose preset (ZenFox = safe everyday speed · AdvancedFox = perf + hardening)" \
  --column="" --column="Preset" --column="Details" \
  TRUE  "ZenFox"     "v157 Balanced · ~63 prefs · low risk · offline" \
  FALSE "AdvancedFox" "perf + privacy/hardening · medium risk · vendored 1.0.0, offline" \
  FALSE "Compare"    "show Zen vs Advanced diff, change nothing") || exit 0

# --- 2. profile ----------------------------------------------------------------
# NOTE: --list-profiles prints "No profiles found." when empty, so only lines
# shaped like "name — /path" count as real profiles.
PROFILES_TXT=$(python3 setup.py --list-profiles 2>/dev/null | grep " — " || true)
if [ -n "$PROFILES_TXT" ]; then
  ROWS=()
  while IFS= read -r line; do
    [ -n "$line" ] && ROWS+=(FALSE "$line")
  done <<< "$PROFILES_TXT"
  ROWS+=(FALSE "Browse for folder…")
  PICK=$(zenity --list --radiolist --title="$TITLE" --width=620 --height=360 \
    --text="Pick Firefox profile" --column="" --column="Profile" "${ROWS[@]}") || exit 0
  if [ "$PICK" = "Browse for folder…" ]; then
    PROFILE=$(zenity --file-selection --directory --title="Pick Firefox profile folder") || exit 0
  else
    # value looks like "name (default) — /path"; take text after last " — "
    PROFILE="${PICK##* — }"
  fi
else
  zenity --info --title="$TITLE" --width=520 \
    --text="No Firefox profiles detected in the usual places." || exit 0
  if zenity --question --title="$TITLE" --width=480 \
       --text="Create a new Firefox profile now?" \
       --ok-label="Create profile" --cancel-label="Pick folder instead"; then
    PROFILE=$(python3 -c "from src.zenfox_install import profiles; print(profiles.create_profile(profiles.choose_creation_root(profiles.data_roots()))['path'])") || {
      zenity --error --title="$TITLE" --text="Could not create a profile." || true
      exit 1
    }
  else
    PROFILE=$(zenity --file-selection --directory --title="Pick Firefox profile folder") || exit 0
  fi
fi

# Guard: never hand a placeholder or non-folder to the backend.
[ -d "$PROFILE" ] || {
  zenity --error --title="$TITLE" --width=480 --text="Not a folder, aborting:\n$PROFILE" || true
  exit 1
}

ARGS=(--profile "$PROFILE" --yes)

# --- 3. preset-specific ---------------------------------------------------------
if [ "$PRESET" = "Compare" ]; then
  OUT=$(python3 setup.py --dry-run 2>&1)
  zenity --text-info --title="$TITLE — compare" --width=640 --height=420 --filename=<(printf '%s' "$OUT")
  exit 0
elif [ "$PRESET" = "ZenFox" ]; then
  ARGS+=(--preset zenfox)
  OPTS=$(zenity --list --checklist --title="$TITLE" --width=480 --height=260 \
    --text="ZenFox options" --column="" --column="Option" -- \
    FALSE "LITE" "Also install LiteFox.js (debloat/UI)" \
    FALSE "SOFT" "Also install Softfox.js (smooth scroll)" \
    FALSE "POLICIES"  "Install policies.json (needs admin)") || exit 0
  # checklist returns selections separated by |
  [[ "$OPTS" == *"LITE"* ]] && ARGS+=(--with-lite)
  [[ "$OPTS" == *"SOFT"* ]] && ARGS+=(--with-soft)
  [[ "$OPTS" == *"POLICIES"* ]] && ARGS+=(--policies)
  # Custom mode: per-section checklist (all pre-checked = stock preset)
  if zenity --question --title="$TITLE" --width=480 \
       --text="Quick install (whole files) or Custom (pick sections)?" \
       --ok-label="Custom" --cancel-label="Quick"; then
    pick_sections() { # $1 = user.js|LiteFox.js → prints comma list or empty
      local file="$1" rows=() line title n
      while IFS=$'\t' read -r f title n; do
        [ "$f" = "$file" ] || continue
        [ "$n" = "0" ] && continue  # skip empty (e.g. POCKET)
        rows+=(TRUE "$title" "$n prefs")
      done < <(python3 setup.py --list-sections)
      local pick
      pick=$(zenity --list --checklist --title="$TITLE — $file sections" \
        --width=560 --height=480 --text="Uncheck sections to exclude" \
        --column="" --column="Section" --column="Prefs" -- "${rows[@]}") || return 1
        # checklist "|" separator → comma list for --sections
      printf '%s' "${pick//|/,}"
    }
    USEC=$(pick_sections "user.js") || exit 0
    if [ -z "$USEC" ]; then
      zenity --error --title="$TITLE" --width=420 \
        --text="All user.js sections unchecked — nothing to install. Aborting." || true
      exit 1
    fi
    ARGS+=(--sections "$USEC")
    if [[ "$OPTS" == *"LITE"* ]]; then
      LSEC=$(pick_sections "LiteFox.js") || exit 0
      if [ -z "$LSEC" ]; then
        zenity --error --title="$TITLE" --width=420 \
          --text="All LiteFox sections unchecked — nothing to install. Aborting." || true
        exit 1
      fi
      ARGS+=(--lite-sections "$LSEC")
    fi
  fi
else
  ARGS+=(--preset advancedfox)
  LEVEL=$(zenity --list --radiolist --title="$TITLE" --width=520 --height=300 \
    --text="AdvancedFox level (vendored 1.0.0, installs offline)" \
    --column="" --column="Level" --column="Notes" -- \
    FALSE "weak"   "light hardening, fewest breakages" \
    TRUE  "medium" "balanced hardening (recommended)" \
    FALSE "strong" "maximum hardening, most breakages") || exit 0
  ARGS+=(--adv-level "$LEVEL")
  if zenity --question --title="$TITLE" --width=480 \
       --text="Install vendored policies.json too? (needs admin)" \
       --ok-label="Yes" --cancel-label="No"; then
    ARGS+=(--policies)
  fi
fi

# --- 4. confirm + run -------------------------------------------------------------
zenity --question --title="$TITLE" --width=480 \
  --text="Install $PRESET into:\n$PROFILE\n\nA timestamped backup is made first. Close Firefox now." || exit 0

LOG=$(mktemp)
if python3 setup.py "${ARGS[@]}" >"$LOG" 2>&1; then
  zenity --text-info --title="$TITLE — done" --width=640 --height=420 --filename="$LOG"
else
  zenity --text-info --title="$TITLE — FAILED" --width=640 --height=420 --filename="$LOG"
fi
rm -f "$LOG"
