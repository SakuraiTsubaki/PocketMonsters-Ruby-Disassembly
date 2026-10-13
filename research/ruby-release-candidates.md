# Ruby release candidates

This foundation pass records twelve distinct retail identities in the local corpus: the Japanese origin release; English revisions 0, 1, and 2; and German, French, Italian, and Spanish revisions 0 and 1. The Japanese input is an observed 8 MiB `AXVJ` image; all global `AXVE`, `AXVD`, `AXVF`, `AXVI`, and `AXVS` images are 16 MiB.

The separately observed German debug build remains in `analysis/ruby-global-release-catalog.json` as historical evidence but is deliberately excluded from the official retail baseline.

Every entry passed the shared Game Boy Advance inspector's Nintendo logo, fixed-value, reserved-area, and header-checksum validation. Hashes and decoded headers are synchronized across the project metadata, release matrix, analysis report, and tests.

All identities remain `candidate`. GBA header integrity does not independently prove canonical retail provenance, and GBA has no whole-ROM checksum comparable to the Game Boy global checksum. Promotion to `verified` therefore requires an independent trusted reference or a reproducible matching build.

No ROM binary or byte extract is included.
