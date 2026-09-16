#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_ROOT="${GEN3_TOOLS_ROOT:-$ROOT_DIR/.tools}"
if [[ -f "$TOOLS_ROOT/activate.sh" ]]; then
  source "$TOOLS_ROOT/activate.sh"
fi

missing=0
ok()   { printf '[OK]   %-24s %s\n' "$1" "$2"; }
fail() { printf '[MISS] %-24s %s\n' "$1" "$2"; missing=1; }

find_cmd() {
  local label=$1; shift
  local cmd
  for cmd in "$@"; do
    if command -v "$cmd" >/dev/null 2>&1; then
      ok "$label" "$(command -v "$cmd")"
      return 0
    fi
  done
  fail "$label" "tried: $*"
  return 1
}

printf 'PocketMonsters-Ruby-Disassembly toolchain check\n'
printf '%s\n' '------------------------------------------------'
find_cmd "Python" python3 || true
find_cmd "Clang" clang || true
find_cmd "LLD" ld.lld || true
find_cmd "LLVM objdump" llvm-objdump || true
find_cmd "LLVM objcopy" llvm-objcopy || true
find_cmd "GNU ARM GCC" arm-none-eabi-gcc || true
find_cmd "GNU ARM assembler" arm-none-eabi-as || true
find_cmd "GNU ARM objdump" arm-none-eabi-objdump || true
find_cmd "GNU ARM objcopy" arm-none-eabi-objcopy || true
find_cmd "ARM GDB" arm-none-eabi-gdb gdb-multiarch || true
find_cmd "CMake" cmake || true
find_cmd "Ninja" ninja || true
find_cmd "Make" make || true
find_cmd "Git" git || true
find_cmd "mGBA" mgba-qt mgba mgba-sdl || true

if command -v clang >/dev/null 2>&1 && command -v llvm-objdump >/dev/null 2>&1; then
  td=$(mktemp -d)
  cat > "$td/probe.s" <<'ASM'
.syntax unified
.cpu arm7tdmi
.thumb
.global probe
probe:
    movs r0, #1
    bx lr
ASM
  if clang --target=armv4t-none-eabi -c "$td/probe.s" -o "$td/probe.o" >/dev/null 2>&1 \
     && llvm-objdump -d --triple=thumbv4t-none-eabi "$td/probe.o" >/dev/null 2>&1; then
    ok "ARM7TDMI LLVM probe" "ARMv4T Thumb assembly/disassembly works"
  else
    fail "ARM7TDMI LLVM probe" "LLVM could not process ARMv4T Thumb code"
  fi
  rm -rf "$td"
fi

if command -v arm-none-eabi-as >/dev/null 2>&1 && command -v arm-none-eabi-objdump >/dev/null 2>&1; then
  td=$(mktemp -d)
  cat > "$td/probe.s" <<'ASM'
.syntax unified
.cpu arm7tdmi
.thumb
.global probe
probe:
    movs r0, #1
    bx lr
ASM
  if arm-none-eabi-as -mcpu=arm7tdmi -mthumb "$td/probe.s" -o "$td/probe.o" >/dev/null 2>&1 \
     && arm-none-eabi-objdump -d "$td/probe.o" >/dev/null 2>&1; then
    ok "ARM7TDMI GNU probe" "GNU Arm assembler/objdump works"
  else
    fail "ARM7TDMI GNU probe" "GNU Arm tools failed the ARM7TDMI probe"
  fi
  rm -rf "$td"
fi

if [[ $missing -ne 0 ]]; then
  printf '\nMissing required tools. Run: ./tools/setup_dev_environment.sh\n' >&2
  exit 1
fi
printf '\nAll required Ruby disassembly tools are available.\n'
