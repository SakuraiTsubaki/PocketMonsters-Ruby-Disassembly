# Pokemon Ruby display and serial interrupt disassembly

`axv-j-rev0-retail` is the Japanese origin reference. All 13 cataloged releases (Japanese, English, German, French, Italian, Spanish) contain exactly one HBlank, VCount and Serial handler matching the `rs` profile. VCount invokes the optional callback. Each handler sets both INTR_CHECK and gMain.intrCheck. Per-release evidence preserves ranges, hashes, validated literals and call order without ROM bytes or instruction halfwords.
