# GBA Disassembly Toolchain

`PocketMonsters-Ruby-Disassembly` targets Pokémon Ruby on the Game Boy Advance: ARM7TDMI / ARMv4T. The repository therefore uses GBA/ARM reverse-engineering tools rather than RGBDS.

## Core environment

The required environment is:

- **LLVM/Clang + LLD** — primary ARMv4T assembly/link path; the existing byte-preserving `INCBIN` verifier already uses `clang --target=armv4t-none-eabi` and `ld.lld`.
- **LLVM objdump/objcopy** — address-aware disassembly and binary inspection.
- **GNU Arm Embedded (`arm-none-eabi-*`)** — independent assembler/compiler/binutils path used for cross-checking reconstruction.
- **GDB multiarch / Arm GDB** — debugger support.
- **Python 3** — ROM inventory, revision diff, ELF-slice, and baseline verification scripts.
- **CMake, Ninja, Make, Git, jq, xxd, file, diffutils, ripgrep** — build and inspection support.
- **mGBA** — primary GBA emulator for boot/runtime verification and debugging workflows.

## Install

On a networked Debian/Ubuntu-style Linux host:

```sh
./tools/setup_dev_environment.sh
```

The script installs the required distro packages, installs mGBA from the distro when available, and falls back to the mGBA 0.10.5 AppImage. It writes a local `.tools/activate.sh`; downloaded/tool binaries remain local and are not committed.

Then validate the environment:

```sh
./tools/check_gba_env.sh
```

The check assembles and disassembles a real ARMv4T Thumb probe with LLVM and GNU Arm tools rather than merely checking executable names.

## Emulator

```sh
./tools/run_mgba.sh /path/to/local/Pokemon-Ruby.gba
```

The wrapper launches the local ROM in mGBA and never copies it into the repository.

## Optional full GBA SDK

A complete devkitPro `gba-dev` installation is optional for utilities outside the current disassembly baseline:

```sh
./tools/setup_dev_environment.sh --with-devkitpro
```

It is not a default dependency because the current project needs ARMv4T assembly/linking, binary inspection, verification, and emulation rather than a complete homebrew SDK.

## Deliberately not installed by default

- **RGBDS** — Game Boy / Game Boy Color toolchain; wrong architecture for Pokémon Ruby.
- **agbcc** — useful for matching C decompilation projects, but this repository is the Disassembly project.
- **Dolphin** — GameCube/Wii emulator; not required to disassemble or run Pokémon Ruby.
- **Ghidra** — useful optional reverse-engineering UI, but not required for the reproducible command-line baseline.

Retail ROMs remain local read-only inputs and are never downloaded or committed by the tool installer.
