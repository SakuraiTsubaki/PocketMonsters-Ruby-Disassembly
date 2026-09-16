# Tools

This is a Game Boy Advance / ARM7TDMI disassembly project.

- `setup_dev_environment.sh` — install the required ARMv4T toolchain and mGBA.
- `bootstrap_env.sh` — compatibility entry point for the same project-specific installer.
- `check_gba_env.sh` — verify executables and run real LLVM/GNU ARM7TDMI probes.
- `run_mgba.sh` — launch a local ROM in mGBA without copying it into the repository.
- `rom_inventory.py` — identify and hash local Ruby ROM inputs.
- `revision_diff.py` — produce reproducible revision-difference records.
- `make_arm_elf_slice.py` — wrap ROM slices for address-aware disassembly.
- `verify_incbin_baseline.py` — build and hash-check byte-preserving local `INCBIN` baselines.

RGBDS, agbcc, and Dolphin are not required by this Ruby Disassembly repository. A full devkitPro `gba-dev` SDK is optional and can be added with `./tools/setup_dev_environment.sh --with-devkitpro`.

See `../docs/TOOLCHAIN.md` and `../manifests/toolchain.yml`.
