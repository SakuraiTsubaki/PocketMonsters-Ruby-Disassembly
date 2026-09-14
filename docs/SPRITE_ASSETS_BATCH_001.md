# Pokémon sprite assets — Batch 001

First visual sprite asset batch for the Ruby disassembly repository.

## Scope

- Species ID: `001` (Bulbasaur / Fushigidane family slot 001)
- Poses: front, back
- Palettes: normal, shiny
- Verified source ROMs: 13
- Source references: 52 (`13 ROMs × 2 poses × 2 palettes`)
- Unique rendered PNG assets: 4
- Duplicate source references deduplicated: 48

All four rendered combinations are byte-identical at the rendered RGBA level across all 13 verified Ruby ROMs. The repository therefore stores one PNG per pose/palette combination, while the manifest preserves every ROM SHA-1, table offset, pointer, decompressed tile SHA-256, palette SHA-256, and rendered SHA-256.

## Files

- `graphics/pokemon/001/*.png` — 4 unique human-viewable PNGs
- `manifests/sprites/001_references.csv` — all 52 source references
- `manifests/sprites/001_unique.csv` — one row per stored PNG
- `manifests/sprites/ruby_sprite_tables.csv` — discovered front/back and normal/shiny table offsets for all 13 ROMs
- `tools/extract_pokemon_sprites.py` — standard-library LZ77 extractor, renderer, and SHA-256 deduplicator

## Upload policy

Sprite assets are committed in small batches. Identical graphics from different languages/revisions are stored once, with provenance retained in manifests. Source ROM binaries remain read-only inputs and are never committed.
