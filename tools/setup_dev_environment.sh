#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_ROOT="${GEN3_TOOLS_ROOT:-$ROOT_DIR/.tools}"
BIN_DIR="$TOOLS_ROOT/bin"
EMU_DIR="$TOOLS_ROOT/emulators"
MGBA_VERSION="${MGBA_VERSION:-0.10.5}"
CHECK_ONLY=0
WITH_DEVKITPRO=0

for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --with-devkitpro) WITH_DEVKITPRO=1 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

log() { printf '[ruby-disassembly] %s\n' "$*"; }
warn() { printf '[ruby-disassembly] WARNING: %s\n' "$*" >&2; }
have() { command -v "$1" >/dev/null 2>&1; }

mkdir -p "$BIN_DIR" "$EMU_DIR"
export PATH="$BIN_DIR:$PATH"

if [[ -f "$TOOLS_ROOT/activate.sh" ]]; then
  source "$TOOLS_ROOT/activate.sh"
fi

if (( CHECK_ONLY )); then
  exec "$ROOT_DIR/tools/check_gba_env.sh"
fi

[[ "$(uname -s)" == Linux ]] || {
  echo "Automatic installation currently targets Linux. Install equivalents from docs/TOOLCHAIN.md, then run --check-only." >&2
  exit 1
}

if [[ "$(id -u)" -eq 0 ]]; then
  SUDO=()
elif have sudo; then
  SUDO=(sudo)
else
  echo "sudo or root privileges are required for package installation." >&2
  exit 1
fi

apt_install() {
  have apt-get || return 1
  DEBIAN_FRONTEND=noninteractive "${SUDO[@]}" apt-get install -y --no-install-recommends "$@"
}

if have apt-get; then
  log "Installing ARM7TDMI/ARMv4T disassembly toolchain..."
  "${SUDO[@]}" apt-get update
  apt_install \
    build-essential ca-certificates curl git file xz-utils unzip jq ripgrep xxd diffutils \
    python3 python3-venv make cmake ninja-build \
    clang lld llvm \
    gcc-arm-none-eabi binutils-arm-none-eabi gdb-multiarch
else
  echo "Unsupported Linux package manager. See docs/TOOLCHAIN.md." >&2
  exit 1
fi

link_bin() {
  local src="$1" name="$2"
  [[ -e "$src" ]] && ln -sfn "$src" "$BIN_DIR/$name"
}

for t in gcc as ld objdump objcopy ar ranlib nm readelf size; do
  p="$(command -v "arm-none-eabi-$t" 2>/dev/null || true)"
  [[ -n "$p" ]] && link_bin "$p" "arm-none-eabi-$t"
done

install_mgba() {
  if have mgba-qt; then
    link_bin "$(command -v mgba-qt)" mgba
    return 0
  fi
  if have mgba; then
    link_bin "$(command -v mgba)" mgba
    return 0
  fi
  if have mgba-sdl; then
    link_bin "$(command -v mgba-sdl)" mgba
    return 0
  fi

  if apt_install mgba-qt >/dev/null 2>&1 || apt_install mgba-sdl >/dev/null 2>&1; then
    if have mgba-qt; then link_bin "$(command -v mgba-qt)" mgba; return 0; fi
    if have mgba-sdl; then link_bin "$(command -v mgba-sdl)" mgba; return 0; fi
  fi

  local arch asset app
  case "$(uname -m)" in
    x86_64|amd64) arch='x64' ;;
    aarch64|arm64) arch='arm64' ;;
    *) warn "unsupported mGBA AppImage architecture: $(uname -m)"; return 1 ;;
  esac
  asset="mGBA-${MGBA_VERSION}-appimage-${arch}.appimage"
  app="$EMU_DIR/$asset"
  if [[ ! -x "$app" ]]; then
    log "Downloading mGBA ${MGBA_VERSION} AppImage..."
    curl -fL --retry 3 --retry-delay 2 \
      "https://github.com/mgba-emu/mgba/releases/download/${MGBA_VERSION}/${asset}" \
      -o "$app"
    chmod +x "$app"
  fi
  link_bin "$app" mgba
}

install_devkitpro() {
  local installer="$TOOLS_ROOT/install-devkitpro-pacman"
  if ! have dkp-pacman && [[ ! -x /opt/devkitpro/pacman/bin/pacman ]]; then
    log "Installing devkitPro package manager (optional GBA SDK)..."
    curl -fL --retry 3 https://apt.devkitpro.org/install-devkitpro-pacman -o "$installer"
    chmod +x "$installer"
    "${SUDO[@]}" "$installer"
  fi
  local pacman
  pacman="$(command -v dkp-pacman 2>/dev/null || true)"
  [[ -n "$pacman" ]] || [[ ! -x /opt/devkitpro/pacman/bin/pacman ]] || pacman=/opt/devkitpro/pacman/bin/pacman
  if [[ -n "$pacman" ]]; then
    "${SUDO[@]}" "$pacman" -Sy --noconfirm
    "${SUDO[@]}" "$pacman" -S --needed --noconfirm gba-dev
  fi
}

install_mgba

if (( WITH_DEVKITPRO )); then
  install_devkitpro
fi

cat > "$TOOLS_ROOT/activate.sh" <<ACTIVATE
export PATH="$BIN_DIR:\$PATH"
ACTIVATE

source "$TOOLS_ROOT/activate.sh"
log "Toolchain installation complete. Running ARM7TDMI checks..."
exec "$ROOT_DIR/tools/check_gba_env.sh"
