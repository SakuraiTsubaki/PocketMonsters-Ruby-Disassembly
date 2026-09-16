#!/usr/bin/env bash
set -euo pipefail

# Pokémon Gen III GBA disassembly environment bootstrap.
# Installs build/disassembly tools and mGBA without committing emulator/tool binaries.

MGBA_VERSION="${MGBA_VERSION:-0.10.5}"
ARM_GNU_VERSION="${ARM_GNU_VERSION:-15.3.rel1}"
WITH_DOLPHIN=0
CHECK_ONLY=0

for arg in "$@"; do
  case "$arg" in
    --with-dolphin) WITH_DOLPHIN=1 ;;
    --check-only) CHECK_ONLY=1 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

have() { command -v "$1" >/dev/null 2>&1; }

check_tools() {
  local missing=0
  for tool in python3 git make cmake ninja clang llvm-objdump ld.lld; do
    if have "$tool"; then
      printf '[ok] %s -> %s\n' "$tool" "$(command -v "$tool")"
    else
      printf '[missing] %s\n' "$tool"
      missing=1
    fi
  done

  if have arm-none-eabi-gcc && have arm-none-eabi-objdump; then
    printf '[ok] Arm GNU toolchain\n'
  else
    printf '[optional-missing] Arm GNU toolchain (LLVM remains usable)\n'
  fi

  if have mgba || have mgba-qt || have mgba-sdl; then
    printf '[ok] mGBA\n'
  elif [[ -x "$HOME/.local/bin/mgba" ]]; then
    printf '[ok] mGBA AppImage -> %s\n' "$HOME/.local/bin/mgba"
  else
    printf '[missing] mGBA\n'
    missing=1
  fi

  if (( WITH_DOLPHIN )); then
    if have dolphin-emu || have dolphin; then
      printf '[ok] Dolphin\n'
    elif have flatpak && flatpak info org.DolphinEmu.dolphin-emu >/dev/null 2>&1; then
      printf '[ok] Dolphin (Flatpak)\n'
    else
      printf '[missing] Dolphin\n'
      missing=1
    fi
  fi

  return "$missing"
}

if (( CHECK_ONLY )); then
  check_tools
  exit $?
fi

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This bootstrap currently targets Linux. Install equivalent tools manually, then run --check-only." >&2
  exit 1
fi

SUDO=""
if [[ "$(id -u)" -ne 0 ]]; then
  if have sudo; then SUDO="sudo"; else echo "sudo is required for distro package installation." >&2; exit 1; fi
fi

if have apt-get; then
  $SUDO apt-get update
  $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ca-certificates curl git file xz-utils unzip jq \
    python3 python3-venv python3-pip \
    make cmake ninja-build \
    clang lld llvm \
    gcc-arm-none-eabi binutils-arm-none-eabi gdb-multiarch || true

  # Prefer distro mGBA when available.
  $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y mgba-qt || \
  $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y mgba-sdl || true
fi

# Official Arm GNU bare-metal toolchain fallback.
if ! have arm-none-eabi-gcc; then
  install_root="$HOME/.local/opt"
  archive="arm-gnu-toolchain-${ARM_GNU_VERSION}-x86_64-arm-none-eabi.tar.xz"
  url="https://developer.arm.com/-/media/Files/downloads/gnu/${ARM_GNU_VERSION}/binrel/${archive}"
  mkdir -p "$install_root" "$HOME/.local/bin"
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  curl -fL "$url" -o "$tmp/$archive"
  tar -xJf "$tmp/$archive" -C "$install_root"
  tool_dir="$install_root/arm-gnu-toolchain-${ARM_GNU_VERSION}-x86_64-arm-none-eabi/bin"
  for exe in "$tool_dir"/*; do
    ln -sf "$exe" "$HOME/.local/bin/$(basename "$exe")"
  done
fi

# Official mGBA AppImage fallback.
if ! have mgba && ! have mgba-qt && ! have mgba-sdl && [[ ! -x "$HOME/.local/bin/mgba" ]]; then
  mkdir -p "$HOME/.local/opt/mgba" "$HOME/.local/bin"
  app="$HOME/.local/opt/mgba/mGBA-${MGBA_VERSION}-x64.AppImage"
  curl -fL "https://github.com/mgba-emu/mgba/releases/download/${MGBA_VERSION}/mGBA-${MGBA_VERSION}-appimage-x64.appimage" -o "$app"
  chmod +x "$app"
  ln -sf "$app" "$HOME/.local/bin/mgba"
fi

# Optional GameCube emulator for cross-title/link testing.
if (( WITH_DOLPHIN )); then
  if have apt-get; then
    $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y dolphin-emu || true
  fi
  if ! have dolphin-emu && ! have dolphin; then
    if ! have flatpak && have apt-get; then
      $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y flatpak || true
    fi
    if have flatpak; then
      flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
      flatpak install --user -y flathub org.DolphinEmu.dolphin-emu
    fi
  fi
fi

export PATH="$HOME/.local/bin:$PATH"

# Prove that the installed compiler can emit ARM7TDMI ARM + Thumb code.
tmp_src="$(mktemp --suffix=.s)"
tmp_obj="$(mktemp --suffix=.o)"
cat >"$tmp_src" <<'ASM'
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
llvm-objdump -d --triple=arm-none-eabi "$tmp_obj" >/dev/null
rm -f "$tmp_src" "$tmp_obj"

echo "ARM7TDMI LLVM smoke test: PASS"
check_tools
