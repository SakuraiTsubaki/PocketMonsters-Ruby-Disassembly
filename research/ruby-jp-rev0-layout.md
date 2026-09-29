# Ruby Japanese revision 0 layout measurement

The 8 MiB Japanese origin candidate `ruby-jp-rev0` is divided into eight 1 MiB measurement regions. `analysis/ruby-jp-rev0-layout.json` records region hashes, entropy, byte counts, candidate GBA ROM pointers (including odd Thumb pointers), and words matching the top-byte pattern of unconditional ARM branch encodings.

Region 0 is labeled only `header-and-entry`; regions 1–7 remain `unclassified`. Pointer and branch-word counts are search signals, not proof that an entire region is code or data. In particular, arbitrary data can match instruction or address bit patterns. Future boundaries must be supported by control-flow decoding, reference targets, known formats, or build reconstruction.

All eight regions contain non-uniform content; no 1 MiB region is classified as padding. No ROM bytes or extracted byte ranges are stored, and the release remains a `candidate` pending independent confirmation.
