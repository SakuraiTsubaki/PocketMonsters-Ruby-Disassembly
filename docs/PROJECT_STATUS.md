# Project Status

## Current stage

**Phase 1 — 13-target inventory complete; bootstrap disassembly active**

All 13 supplied Pokémon Ruby ROM inputs have been inventoried read-only. Their MD5/SHA-1/SHA-256 hashes, GBA cartridge headers, software revisions, entry branches, and bootstrap families are recorded. All 13 GBA header complement checks validate. ROM binaries remain excluded from GitHub.

| Area | Status |
| --- | --- |
| Version/revision inventory | **13/13 complete** |
| Cartridge header verification | **13/13 complete** |
| ARM entry/bootstrap mapping | **Started; two verified layout families** |
| Thumb entry mapping | **Started** |
| Small retail revision diff | **Instruction-level verified** |
| ROM / section mapping | In progress |
| Code reconstruction | In progress from bootstrap/IRQ path |
| Data reconstruction | Pending range classification |
| Scripts / events | Pending range classification |
| Graphics / assets | Pending range classification |
| Audio / resources | Pending range classification |
| Maps / world data | Pending range classification |
| Byte-preserving INCBIN baseline | **13/13 SHA-256 matching** |
| Matching build | Pending |

## Verified bootstrap split

Japan and English builds branch from `0x08000000` to ARM code at `0x080000D0` and enter Thumb at `0x0800024C`. German/French/Italian/Spanish builds branch to ARM code at `0x08000204` and enter Thumb at `0x08000380`, with a target-specific metadata/pointer area before the code.

Japan uses IRQ dispatch table RAM `0x03001B30`; international retail uses `0x03001BC0`; the German debug-designated build uses `0x03001C40`.

## Revision finding

German/French/Italian/Spanish Rev 0 -> Rev 1 differs by only four bytes total: software revision, header complement check, and two Thumb condition-code bytes (`BLE -> BLT`, `BGT -> BGE`). English Rev 1 -> Rev 2 contains the same logical instruction pair at the English addresses and likewise differs by four bytes total.

## Immediate continuation

The `INCBIN` reconstruction baseline is verified for all 13 targets. Next, replace the verified ARM bootstrap, IRQ handler, and first Thumb functions with labeled source while checking byte identity after every replacement.
