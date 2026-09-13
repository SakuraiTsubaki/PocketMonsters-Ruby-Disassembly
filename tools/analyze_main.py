#!/usr/bin/env python3
"""Map the symbolized main.c startup region for verified Pokémon Ruby ROMs.

This tool never writes ROM data. It verifies each local ROM against
manifests/source_roms.json, then emits function boundaries, hashes, and
addresses for the AgbMain..ClearPokemonCrySongs region.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROM_BASE = 0x08000000

INTERNATIONAL_LAYOUT = [
    ("AgbMain", 0x000),
    ("UpdateLinkAndCallCallbacks", 0x0F4),
    ("InitMainCallbacks", 0x13C),
    ("CallCallbacks", 0x15C),
    ("SetMainCallback2", 0x180),
    ("SeedRngWithRtc", 0x198),
    ("InitKeys", 0x1B4),
    ("ReadKeys", 0x1DC),
    ("InitIntrHandlers", 0x278),
    ("SetVBlankCallback", 0x2F4),
    ("SetHBlankCallback", 0x300),
    ("SetVCountCallback", 0x30C),
    ("SetSerialCallback", 0x318),
    ("VBlankIntr", 0x324),
    ("InitFlashTimer", 0x3A0),
    ("HBlankIntr", 0x3B4),
    ("VCountIntr", 0x3E4),
    ("SerialIntr", 0x414),
    ("IntrDummy", 0x444),
    ("WaitForVBlank", 0x448),
    ("DoSoftReset", 0x468),
    ("ClearPokemonCrySongs", 0x4D8),
    ("__next_object_start", 0x4FC),
]

JAPAN_LAYOUT = [
    ("AgbMain", 0x000),
    ("UpdateLinkAndCallCallbacks", 0x0FC),
    ("InitMainCallbacks", 0x144),
    ("CallCallbacks", 0x164),
    ("SetMainCallback2", 0x188),
    ("SeedRngWithRtc", 0x19C),
    ("InitKeys", 0x1B8),
    ("ReadKeys", 0x1E0),
    ("InitIntrHandlers", 0x27C),
    ("SetVBlankCallback", 0x2F8),
    ("SetHBlankCallback", 0x304),
    ("SetVCountCallback", 0x310),
    ("SetSerialCallback", 0x31C),
    ("VBlankIntr", 0x328),
    ("InitFlashTimer", 0x3A4),
    ("HBlankIntr", 0x3B8),
    ("VCountIntr", 0x3E8),
    ("SerialIntr", 0x418),
    ("IntrDummy", 0x448),
    ("WaitForVBlank", 0x44C),
    ("DoSoftReset", 0x46C),
    ("ClearPokemonCrySongs", 0x4DC),
    ("__next_object_start", 0x500),
]


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_hex(value: str) -> int:
    return int(value, 16)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom-dir", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, default=Path("manifests/source_roms.json"))
    parser.add_argument("--startup-manifest", type=Path, default=Path("manifests/startup_phase2.json"))
    parser.add_argument("--out-manifest", type=Path, default=Path("manifests/main_phase2.json"))
    parser.add_argument("--out-symbols", type=Path, default=Path("symbols/main_symbols.csv"))
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    source = load_json(args.source_manifest)
    startup = load_json(args.startup_manifest)
    source_by_id = {row["id"]: row for row in source["roms"]}

    result = {
        "schema_version": 1,
        "scope": "main.c symbolized reconstruction from AgbMain through ClearPokemonCrySongs",
        "address_base": f"0x{ROM_BASE:08X}",
        "targets": {},
    }
    csv_rows = []

    for target_id, start_info in startup["targets"].items():
        src = source_by_id[target_id]
        rom_path = args.rom_dir / src["file"]
        data = rom_path.read_bytes()

        actual_sha1 = sha1(data)
        if actual_sha1 != src["sha1"]:
            raise SystemExit(
                f"{target_id}: SHA-1 mismatch: expected {src['sha1']}, got {actual_sha1}"
            )

        agbmain = parse_hex(start_info["agbmain_offset"])
        family = "japan" if target_id == "japan_rev0" else "international"
        layout = JAPAN_LAYOUT if family == "japan" else INTERNATIONAL_LAYOUT

        functions = []
        for (name, rel), (_, next_rel) in zip(layout, layout[1:]):
            start = agbmain + rel
            end = agbmain + next_rel
            chunk = data[start:end]
            entry = {
                "symbol": name,
                "file_offset": f"0x{start:X}",
                "address": f"0x{ROM_BASE + start:08X}",
                "thumb_address": f"0x{ROM_BASE + start + 1:08X}",
                "size": len(chunk),
                "sha1": sha1(chunk),
            }
            functions.append(entry)
            csv_rows.append(
                [
                    target_id,
                    family,
                    name,
                    entry["file_offset"],
                    entry["address"],
                    entry["thumb_address"],
                    entry["size"],
                    entry["sha1"],
                ]
            )

        region_end = agbmain + layout[-1][1]
        region = data[agbmain:region_end]
        result["targets"][target_id] = {
            "family": family,
            "agbmain_offset": f"0x{agbmain:X}",
            "main_region_end_offset": f"0x{region_end:X}",
            "main_region_size": len(region),
            "main_region_sha1": sha1(region),
            "functions": functions,
        }

    if args.verify_only:
        print(f"verified {len(result['targets'])} targets")
        return 0

    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_symbols.parent.mkdir(parents=True, exist_ok=True)

    args.out_manifest.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    with args.out_symbols.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp, lineterminator="\n")
        writer.writerow(
            [
                "target",
                "family",
                "symbol",
                "file_offset",
                "address",
                "thumb_address",
                "size",
                "sha1",
            ]
        )
        writer.writerows(csv_rows)

    print(f"wrote {args.out_manifest}")
    print(f"wrote {args.out_symbols}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
