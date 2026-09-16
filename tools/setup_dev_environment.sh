#!/usr/bin/env bash
set -euo pipefail

# Pokemon Generation III GBA disassembly environment bootstrap.
# Toolchains/emulators only; ROM/disc images are never downloaded.

MGBA_VERSION="${MGBA_VERSION:-0.10.5}"
TOOLS_ROOT="${GEN3_TOOLS_ROOT:-$HOME/.local/share/pokemon-gen3-tools}"
BIN_DIR="${GEN3_BIN_DIR:-$HOME/.local/bin}"
CHECK_ONLY=0
WITH_DOLPHIN=1

for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --no-dolphin) WITH_DOLPHIN=0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

have() { command -v "$1" >/dev/null 2>&1; }
root() { if [[ "$(id -u)" -eq 0 ]]; then "$@"; else sudo "$@"; fi; }
fetch() { if have curl; then curl -fL --retry 3 "$1" -o "$2"; else wget -O "$2" "$1"; fi; }

check_tools() {
  local missing=0
  for tool in python3 git make cmake ninja clang llvm-objdump; do
    if have "$tool"; then printf '[ok] %s -> %s\n' "$tool" "$(command -v "$tool")"; else printf '[missing] %s\n' "$tool"; missing=1; fi
  done
  if have arm-none-eabi-gcc && have arm-none-eabi-objdump; then printf '[ok] Arm GNU toolchain\n'; else printf '[optional-missing] Arm GNU toolchain (LLVM remains usable)\n'; fi
  if have mgba || have mgba-qt || have mgba-sdl || [[ -x "$BIN_DIR/mgba" ]]; then printf '[ok] mGBA\n'; else printf '[missing] mGBA\n'; missing=1; fi
  if (( WITH_DOLPHIN )); then
    if have dolphin-emu || have dolphin || { have flatpak && flatpak info --user org.DolphinEmu.dolphin-emu >/dev/null 2>&1; }; then printf '[ok] Dolphin\n'; else printf '[missing] Dolphin\n'; missing=1; fi
  fi
  return "$missing"
}

if (( CHECK_ONLY )); then check_tools; exit $?; fi
[[ "$(uname -s)" == Linux ]] || { echo "Linux bootstrap only; install equivalents then use --check-only." >&2; exit 1; }
mkdir -p "$TOOLS_ROOT" "$BIN_DIR"; export PATH="$BIN_DIR:$PATH"

if have apt-get; then
  root apt-get update
  root env DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential ca-certificates curl wget git file xz-utils unzip jq ripgrep xxd \
    python3 python3-pip python3-venv make cmake ninja-build \
    clang lld llvm gcc-arm-none-eabi binutils-arm-none-eabi gdb-multiarch flatpak || true
fi

if ! have dkp-pacman && [[ ! -x /opt/devkitpro/pacman/bin/pacman ]]; then
  fetch https://apt.devkitpro.org/install-devkitpro-pacman "$TOOLS_ROOT/install-devkitpro-pacman"
  chmod +x "$TOOLS_ROOT/install-devkitpro-pacman"
  root "$TOOLS_ROOT/install-devkitpro-pacman"
fi
DKP_PACMAN="$(command -v dkp-pacman 2>/dev/null || true)"
[[ -n "$DKP_PACMAN" ]] || [[ ! -x /opt/devkitpro/pacman/bin/pacman ]] || DKP_PACMAN=/opt/devkitpro/pacman/bin/pacman
if [[ -n "$DKP_PACMAN" ]]; then
  root "$DKP_PACMAN" -Sy --noconfirm
  root "$DKP_PACMAN" -S --needed --noconfirm gba-dev
fi
[[ -f /etc/profile.d/devkit-env.sh ]] && source /etc/profile.d/devkit-env.sh || true

if ! have mgba && ! have mgba-qt && ! have mgba-sdl && have apt-get; then
  root env DEBIAN_FRONTEND=noninteractive apt-get install -y mgba-qt >/dev/null 2>&1 || \
  root env DEBIAN_FRONTEND=noninteractive apt-get install -y mgba-sdl >/dev/null 2>&1 || true
fi
if ! have mgba && ! have mgba-qt && ! have mgba-sdl; then
  case "$(uname -m)" in x86_64|amd64) arch=x64 ;; aarch64|arm64) arch=arm64 ;; *) arch= ;; esac
  if [[ -n "$arch" ]]; then
    app="$TOOLS_ROOT/mGBA-${MGBA_VERSION}-appimage-${arch}.appimage"
    [[ -f "$app" ]] || fetch "https://github.com/mgba-emu/mgba/releases/download/${MGBA_VERSION}/mGBA-${MGBA_VERSION}-appimage-${arch}.appimage" "$app"
    chmod +x "$app"; ln -sf "$app" "$BIN_DIR/mgba"
  fi
fi

if (( WITH_DOLPHIN )) && ! have dolphin-emu && ! have dolphin && have flatpak; then
  flatpak remote-add --user --if-not-exists dolphin https://flatpak.dolphin-emu.org/releases.flatpakrepo
  flatpak install --user -y dolphin org.DolphinEmu.dolphin-emu
  printf '%s\n' '#!/usr/bin/env bash' 'exec flatpak run org.DolphinEmu.dolphin-emu "$@"' > "$BIN_DIR/dolphin-emu"
  chmod +x "$BIN_DIR/dolphin-emu"
fi

tmp_src="$(mktemp --suffix=.s)"; tmp_obj="$(mktemp --suffix=.o)"
cat > "$tmp_src" <<'ASM'
.syntax unified
.arm
.global _gen3_arm_test
_gen3_arm_test:
    mov r0, #0
    bx lr
.thumb
.global _gen3_thumb_test
_gen3_thumb_test:
    movs r0, #1
    bx lr
ASM
clang --target=arm-none-eabi -mcpu=arm7tdmi -c "$tmp_src" -o "$tmp_obj"
llvm-objdump -d --triple=armv4t-none-eabi "$tmp_obj" >/dev/null
rm -f "$tmp_src" "$tmp_obj"
echo "ARM7TDMI LLVM smoke test: PASS"
check_tools
