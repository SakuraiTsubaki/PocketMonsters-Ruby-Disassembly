#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_ROOT="${GEN3_TOOLS_ROOT:-$ROOT_DIR/.tools}"
if [[ -f "$TOOLS_ROOT/activate.sh" ]]; then
  source "$TOOLS_ROOT/activate.sh"
fi

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <local-rom.gba> [mGBA options...]" >&2
  exit 2
fi
rom=$1
shift
[[ -f "$rom" ]] || { echo "ROM not found: $rom" >&2; exit 1; }

for emu in mgba-qt mgba mgba-sdl; do
  if command -v "$emu" >/dev/null 2>&1; then
    exec "$emu" "$rom" "$@"
  fi
done

echo "mGBA is not installed. Run ./tools/setup_dev_environment.sh" >&2
exit 1
