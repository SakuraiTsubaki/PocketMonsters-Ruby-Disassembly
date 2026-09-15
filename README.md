# Pocket Monsters Ruby — Disassembly

![Status](https://img.shields.io/badge/status-active-blue)
![Project](https://img.shields.io/badge/project-disassembly-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Disassembly and source-reconstruction project for **Pokémon Ruby**.

## 🎯 Goals

- Reconstruct game code and data into readable, editable assembly/source form.
- Document ROM, section, data, script, asset, and version differences.
- Keep analysis, tooling, metadata, and documentation reproducible.
- Build a clean foundation for long-term reverse-engineering work.

## 🚧 Status

Phase 1 target inventory is complete for the 13 supplied read-only Ruby ROM targets. Architecture mapping and source reconstruction are active from the verified ARM bootstrap, IRQ path, and first Thumb entry paths. Exact-byte `INCBIN` baselines are verified for all 13 targets.

## 🗂️ Current project areas

- `asm/` — verified disassembly listings and progressively reconstructed assembly
- `docs/` — project status, architecture findings, version coverage, research, and verification notes
- `manifests/` — target identity, hashes, revision differences, baseline verification, and work queue
- `tools/` — reproducible inventory, diff, disassembly-slice, and baseline-verification tooling

Additional areas such as `data/`, `assets/`, and `tests/` are added only when verified project material exists.

## 📌 Repository policy

ROM images and redistributed ROM binaries are **not included**. Local originals are read-only inputs for hashing, extraction, comparison, reconstruction, and matching verification. The repository contains reconstructed source, extracted/recreated project data, tooling, analysis, manifests, and documentation.

## 🧭 Roadmap

- [x] Establish baseline version/revision inventory
- [ ] Map ROM, section, code, and data structures
- [ ] Reconstruct code, data, scripts, and text
- [ ] Document and reconstruct assets and higher-level systems
- [ ] Complete matching-build and regression verification workflow
- [ ] Expand verified coverage across regional/revision differences

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Project status](docs/PROJECT_STATUS.md) | Current stage, coverage, validation level, and next milestones |
| [Bootstrap findings](docs/BOOTSTRAP.md) | Verified ARM/Thumb startup layout and target-family differences |
| [Roadmap](docs/ROADMAP.md) | Recommended disassembly phases and long-term progression |
| [Version coverage](docs/VERSIONS.md) | Regions, languages, revisions, releases, and hashes |
| [Research guide](docs/RESEARCH_GUIDE.md) | Evidence, confidence, and research-recording workflow |
| [Verification guide](docs/VERIFICATION.md) | Standards for Observed, Reproduced, and Matched results |
| [Repository structure](docs/REPOSITORY_STRUCTURE.md) | Intended long-term source, data, asset, tooling, and manifest layout |
| [Documentation hub](docs/README.md) | Entry point for format, code, script, asset, version, and verification notes |

## 🧱 Repository structure

This is already a single-game Ruby repository. Real project material is organized directly under responsibility-based root areas such as `asm/`, `data/`, `assets/`, `tools/`, `tests/`, `manifests/`, and `docs/`. Target region/language/revision identity is retained in filenames, manifests, metadata, or subpaths where the verified material requires it; no redundant generation/game wrapper is imposed inside this repository.

See [Repository Structure](docs/REPOSITORY_STRUCTURE.md) for the organization policy.

## 🔬 Research and verification

Research findings identify the relevant target version or revision and clearly separate hypotheses from observed, reproduced, or matched results. Use the repository's Research and Verification issue templates when tracking substantial findings.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules, evidence expectations, commit guidance, and pull-request requirements.
