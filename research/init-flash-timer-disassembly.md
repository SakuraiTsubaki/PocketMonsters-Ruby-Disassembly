# Ruby InitFlashTimer disassembly

`axv-j-rev0-retail` is the Japanese origin reference. All 13 cataloged releases (Japanese, English, German, French, Italian, Spanish) independently trace the InitFlashTimer call and preserve the `loaded-handler` operand form for the gFlashTimerIntrFunc handler value. The routine selects timer 2 and calls SetFlashTimerIntr. Per-release maps publish addresses, structure and hashes, never ROM bytes or halfwords.
