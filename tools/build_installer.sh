#!/usr/bin/env bash
# Thin wrapper kept for backward compatibility — real logic lives in
# tools/build_installer.py (OS-correct --add-data separator, --windowed flag).
# Usage: bash tools/build_installer.sh [--windowed] [--name NAME]
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 tools/build_installer.py "$@"
