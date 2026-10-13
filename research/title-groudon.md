# Ruby Japanese title-screen Groudon tiles

The Japanese revision-0 candidate (`AXVJ`, ROM SHA-256
`e911caa1ffbf8704cd45bbe064ade40e24efa50dfdce82adf4b2899b5f733852`)
contains a GBA BIOS-LZ77 stream at `0x36F110`.

Decompression produces 8,192 bytes (256 GBA 4bpp tiles) with SHA-256
`93c1ec4ecac6e99d33dbc47fb84a2350b11a01d578066744f79d506cc48ca862`.
Independently converting `pret/pokeruby`'s indexed
`graphics/title_screen/groudon.png` in 8x8 tile order produces exactly the
same byte digest. This establishes the source/ROM correspondence without
publishing the compressed stream or any raw ROM fragment.

`graphics/title/groudon-dark.png` is a deterministic 2x tile-sheet rendering
using the public `groudon_dark.pal` JASC palette. The image is a tile sheet,
not a composed screenshot; map reconstruction is tracked separately.

Reproduce with the common `SakuraiTsubaki/Disassembly` tool:

```text
extract_gba_lz77_4bpp.py <ROM> --offset 0x36F110 --tiles-per-row 16 \
  --expected-sha256 e911caa1ffbf8704cd45bbe064ade40e24efa50dfdce82adf4b2899b5f733852 \
  --palette graphics/title/groudon-dark.pal \
  --png graphics/title/groudon-dark.png \
  --report analysis/ruby-jp-rev0-title-groudon.json
```

This verifies the asset correspondence only. It does not promote the overall
release candidate to `verified`.

## Whole-ROM discovery evidence

A bounded scan of the complete 8 MiB Japanese ROM found 54 valid BIOS-LZ77
streams with an 8,192-byte decoded length, all with distinct decoded hashes.
The equivalent Sapphire scan also found 54. Exactly 53 decoded hashes are
shared; Ruby's sole unmatched stream is the Groudon stream at `0x36F110`, and
Sapphire's sole unmatched stream is the independently identified Kyogre
stream. `analysis/ruby-jp-rev0-lz77-8192-scan.json` preserves the offsets,
lengths, and hashes for reproduction without publishing ROM bytes.
