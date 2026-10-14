# Title-screen Groudon across later retail revisions

The English rev1/rev2 and German, French, Italian, and Spanish rev1 ROMs were each gated by their release-catalog SHA-256 before scanning. In every case exactly one BIOS-LZ77 stream decodes to the established 8,192-byte Groudon tile hash `93c1ec4ecac6e99d33dbc47fb84a2350b11a01d578066744f79d506cc48ca862`.

The compressed stream is byte-identical across all six later revisions (`19502e66c1a9d95332ede0f4f2df5a0e62adb71adca82ffdcb85ae83f021ccc2`) but occurs at release-specific offsets. Re-extraction with the verified palette reproduces the existing color PNG exactly. Each stream has one stored pointer and one direct Thumb consumer which loads destination VRAM `0x06008000` before calling its release-local LZ77 routine.

These reports extend asset and runtime provenance to all 12 catalogued retail releases. Candidate release status is unchanged; no ROM bytes are published.
