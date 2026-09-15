# Repository Structure

The live project path convention is:

`GENERATION → GAME → LANGUAGE/REGION → REVISION → WORK TYPE`

For this repository the concrete root is `GENERATION_III/RUBY/`. Target-specific material belongs below a language/region and revision directory. Cross-target inventories and tools use the explicit aggregate path `MULTI_REGION/ALL_REVISIONS/`; this preserves the same hierarchy without pretending that a shared artifact belongs to one retail target.

Examples:

- `GENERATION_III/RUBY/JAPAN_JAPANESE/REV_0/DISASSEMBLY/`
- `GENERATION_III/RUBY/USA_ENGLISH/REV_0/DISASSEMBLY/`
- `GENERATION_III/RUBY/EUROPE_GERMAN/REV_1/DISASSEMBLY/`
- `GENERATION_III/RUBY/MULTI_REGION/ALL_REVISIONS/MANIFESTS/`
- `GENERATION_III/RUBY/MULTI_REGION/ALL_REVISIONS/TOOLS/`

Work types may include `DISASSEMBLY`, `MANIFESTS`, `ANALYSIS`, `SYMBOLS`, `MAPS`, `SCRIPTS`, `GRAPHICS`, `AUDIO`, `TESTS`, and `BUILD`, created only when verified project material exists.

ROM binaries are never committed. Local original ROMs are read-only inputs for hashing, extraction, comparison, `INCBIN` baselines, and matching verification.
