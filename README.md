# PocketMonsters-Ruby-Disassembly

Reproducible disassembly/decompilation workspace for **Pokémon Ruby**.

The goal of this repository is to reconstruct the game from editable source-form assets and code so that supported versions can eventually be rebuilt **without requiring a local source ROM**.

## Project goals

- Preserve original ROMs as read-only reference material outside Git.
- Reconstruct code as C/ASM and progressively eliminate opaque ROM-backed `incbin` regions.
- Extract and restore game data into editable source formats.
- Restore graphics as viewable assets (PNG where practical) plus palettes/tile data and conversion rules.
- Restore text, scripts, maps, events, Pokémon data, moves, items, trainers, encounters, and other tables.
- Restore music, cries, samples, and sound metadata in editable/rebuildable forms such as MIDI/WAV/source tables where practical.
- Track language- and revision-specific differences explicitly.
- Verify rebuilt ROMs against known hashes for each supported version.
- Keep generated ROM binaries out of Git.

## Target material

The project is designed to cover the available Pokémon Ruby language/revision set, including Japanese, English/USA/Europe, German, French, Italian, and Spanish releases and known revisions/debug variants represented by the project's verified source ROM set.

Version-specific material belongs under `config/versions/`, `data/versions/`, or another clearly scoped version directory rather than being duplicated without documentation.

## Repository policy

### Included

- C / ASM source
- linker/build configuration
- constants and headers
- structured game data
- maps and event scripts
- decoded text and character tables
- reconstructed graphics and palettes
- human-viewable sprite/graphics PNGs
- music/MIDI, cries/WAV, samples, and sound source data
- extraction/conversion/build/verification tools
- manifests, hashes, symbol maps, logs, documentation, and tests
- patches and other non-ROM reproducibility artifacts

### Not included

- original retail ROM images
- modified ROM images
- rebuilt/generated ROM images
- other complete game ROM binaries

Generated `.gba` files are build outputs only and must remain ignored by Git.

## Planned layout

```text
asm/                 low-level assembly and remaining reconstructed sections
src/                 decompiled C source
include/             headers
constants/           constants and IDs
data/                 structured game data
  versions/           language/revision-specific data
graphics/             reconstructed graphics, sprites, palettes, tiles
sound/                music, cries, samples, sound tables
maps/                 map/layout/event source where separated from data
text/                 decoded/localized text where separated from data
tools/                extraction, conversion, build and verification tools
config/versions/      per-version build configuration
manifests/            hashes, inventories and provenance manifests
symbols/              symbol/address maps
docs/                 reverse-engineering and format documentation
tests/                regression and rebuild verification
build/                generated files (ignored)
```

Directories will be populated as material is reconstructed; empty placeholder directories are intentionally avoided.

## Reproducibility target

For each supported version:

```text
repository source
      ↓ build
rebuilt .gba
      ↓ checksum verification
known reference hash
      ↓
byte-identical match
```

Until a version reaches a fully reconstructed state, its manifest should clearly identify unresolved regions and verification status.

## Status

Repository initialized. Source-ROM inventory, hashes, ROM layout analysis, and reconstruction manifests are the first implementation stage.
