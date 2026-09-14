# Pokémon sprite assets — Batch 002

Small sprite asset batch for the Ruby disassembly repository.

## Scope

- Species ID: `002` (Ivysaur / Fushigisou)
- Poses: front, back
- Palettes: normal, shiny
- Verified source ROMs: 13
- Source references: 52 (`13 ROMs × 2 poses × 2 palettes`)
- Unique rendered PNG assets: 4
- Duplicate source references deduplicated: 48

All four rendered combinations are byte-identical at the rendered RGBA level across all 13 verified Ruby ROMs. The repository therefore stores one PNG per pose/palette combination, while the manifest preserves the ROM target, source pointers, and asset mapping.

## Files

- `graphics/pokemon/002/*.png` — 4 unique human-viewable PNGs
- `manifests/sprites/002_references.csv` — all 52 source references
- `manifests/sprites/002_unique.csv` — one row per stored PNG

## Upload policy

Sprite assets are committed in small batches. Identical graphics from different languages/revisions are stored once, with provenance retained in manifests. Source ROM binaries remain read-only inputs and are never committed.
