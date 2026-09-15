# Ruby bootstrap disassembly map

This is the first verified code map produced directly from the 13 read-only Ruby ROM inputs. Addresses are GBA ROM virtual addresses (`0x08000000` base). Unknown regions remain unnamed.

## Bootstrap family A — Japan / English

- ROM entry at `0x08000000`: ARM `B 0x080000D0`.
- ARM bootstrap starts at `0x080000D0`.
- SVC stack literal: `0x03007E60`.
- System stack literal: `0x03007FA0`.
- IRQ handler begins at `0x0800010C`.
- IRQ callback/vector pointer is installed at `0x03007FFC`.
- The ARM bootstrap branches through literal `0x0800024D`, entering Thumb code at aligned address `0x0800024C`.
- Interrupt dispatch table RAM pointer differs by target: Japan uses `0x03001B30`; English retail revisions use `0x03001BC0`.

## Bootstrap family B — localized European builds

German, French, Italian, and Spanish retail ROMs, plus the German debug-designated ROM, use a relocated bootstrap:

- ROM entry at `0x08000000`: ARM `B 0x08000204`.
- `0x0000D0..0x0000FF` is `0xFF` padding in the verified retail localized inputs.
- A target-specific metadata/pointer block occupies the `0x000100` area before code. It includes the ASCII string `pokemon ruby version`; its semantics are intentionally not guessed yet.
- ARM bootstrap starts at `0x08000204`.
- IRQ handler begins at `0x08000240`.
- IRQ callback/vector pointer is installed at `0x03007FFC`.
- The ARM bootstrap branches through literal `0x08000381`, entering Thumb code at aligned address `0x08000380`.
- Retail localized ROMs use interrupt dispatch table RAM `0x03001BC0`; the German debug-designated ROM uses `0x03001C40`.

## First revision patch isolated

The small retail revision update is now instruction-level verified. For German/French/Italian/Spanish Rev 0 -> Rev 1, only four bytes differ in the entire 16 MiB ROM: the header revision/check byte and two Thumb condition-code bytes. The two code changes are `BLE -> BLT` at `0x08009366` and `BGT -> BGE` at `0x0800938A`.

English Rev 1 -> Rev 2 has the same logical two-instruction change at `0x0800919A` and `0x080091BE`, plus the two header bytes.

## Next disassembly pass

1. Split verified header/bootstrap/Thumb-main ranges from opaque data ranges.
2. Replace only verified code with labeled ARM/Thumb source; preserve all unresolved bytes with offset-bounded `INCBIN` ranges.
3. Build per-target address maps instead of assuming offsets are shared between Japan, English, localized retail, and debug builds.
4. Continue control-flow discovery outward from the first Thumb entry and IRQ dispatch path.
