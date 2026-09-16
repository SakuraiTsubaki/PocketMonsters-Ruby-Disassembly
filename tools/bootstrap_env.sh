#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export PROJECT_ROOT="$ROOT_DIR"
BOOTSTRAP_COMMIT="d52b32cf20795033a93b19c073745e64fac33512"
BOOTSTRAP_URL="https://raw.githubusercontent.com/SakuraiTsubaki/Sakurai/${BOOTSTRAP_COMMIT}/tools/bootstrap_env.sh"
TMP_FILE="$(mktemp)"
trap 'rm -f "$TMP_FILE"' EXIT
curl --fail --silent --show-error --location "$BOOTSTRAP_URL" --output "$TMP_FILE"
sha256sum "$TMP_FILE" >/dev/null
bash "$TMP_FILE"
