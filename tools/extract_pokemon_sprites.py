#!/usr/bin/env python3
"""Extract and deduplicate Pokémon front/back sprites from Pokémon Ruby GBA ROMs.

The script discovers the two CompressedSpriteSheet tables (front/back) and the
two CompressedSpritePalette tables (normal/shiny) by their sequential tags,
decompresses GBA LZ77 data, renders 64x64 RGBA PNGs, and deduplicates rendered
assets by SHA-256.

Only derived assets/manifests are written. Source ROMs are read-only inputs.
"""
from __future__ import annotations

import argparse
import binascii
import csv
import hashlib
import struct
import zlib
from pathlib import Path


ROM_BASE = 0x08000000


def lz77_decompress_gba(data: bytes, offset: int) -> tuple[bytes, int]:
    if data[offset] != 0x10:
        raise ValueError(f"expected GBA LZ77 header at 0x{offset:X}")
    out_len = data[offset + 1] | (data[offset + 2] << 8) | (data[offset + 3] << 16)
    src = offset + 4
    out = bytearray()

    while len(out) < out_len:
        flags = data[src]
        src += 1
        for bit in range(7, -1, -1):
            if len(out) >= out_len:
                break
            if not (flags & (1 << bit)):
                out.append(data[src])
                src += 1
            else:
                b1, b2 = data[src], data[src + 1]
                src += 2
                length = (b1 >> 4) + 3
                displacement = (((b1 & 0x0F) << 8) | b2) + 1
                for _ in range(length):
                    out.append(out[-displacement])
                    if len(out) >= out_len:
                        break

    return bytes(out), src - offset


def find_sprite_tables(data: bytes, check_entries: int = 20) -> tuple[list[int], list[int]]:
    pic_tables: list[int] = []
    palette_tables: list[int] = []

    for offset in range(0, len(data) - 8 * check_entries, 4):
        ptr, size, tag = struct.unpack_from("<IHH", data, offset)
        if ROM_BASE <= ptr < ROM_BASE + len(data) and size == 0x800 and tag == 0:
            if all(
                ROM_BASE <= p < ROM_BASE + len(data) and s == 0x800 and t == i
                for i in range(check_entries)
                for p, s, t in [struct.unpack_from("<IHH", data, offset + 8 * i)]
            ):
                pic_tables.append(offset)

        ptr, tag, padding = struct.unpack_from("<IHH", data, offset)
        if ROM_BASE <= ptr < ROM_BASE + len(data) and tag == 0 and padding == 0:
            if all(
                ROM_BASE <= p < ROM_BASE + len(data) and t == i and pad == 0
                for i in range(check_entries)
                for p, t, pad in [struct.unpack_from("<IHH", data, offset + 8 * i)]
            ):
                palette_tables.append(offset)

    if len(pic_tables) != 2 or len(palette_tables) != 2:
        raise ValueError(
            f"expected 2 picture tables and 2 palette tables, got "
            f"{len(pic_tables)} and {len(palette_tables)}"
        )
    return pic_tables, palette_tables


def bgr555_to_rgba(value: int, transparent: bool = False) -> bytes:
    r = (value & 0x1F) * 255 // 31
    g = ((value >> 5) & 0x1F) * 255 // 31
    b = ((value >> 10) & 0x1F) * 255 // 31
    return bytes((r, g, b, 0 if transparent else 255))


def render_4bpp_64(tile_data: bytes, palette_data: bytes) -> bytes:
    if len(tile_data) < 0x800 or len(palette_data) < 32:
        raise ValueError("unexpected sprite or palette size")

    palette = [
        bgr555_to_rgba(struct.unpack_from("<H", palette_data, i * 2)[0], transparent=(i == 0))
        for i in range(16)
    ]
    rgba = bytearray(64 * 64 * 4)

    for tile_y in range(8):
        for tile_x in range(8):
            tile_base = (tile_y * 8 + tile_x) * 32
            for y in range(8):
                for x_pair in range(4):
                    value = tile_data[tile_base + y * 4 + x_pair]
                    for k, index in enumerate((value & 0x0F, value >> 4)):
                        x = tile_x * 8 + x_pair * 2 + k
                        out_y = tile_y * 8 + y
                        pos = (out_y * 64 + x) * 4
                        rgba[pos:pos + 4] = palette[index]
    return bytes(rgba)


def png_bytes_rgba(width: int, height: int, rgba: bytes) -> bytes:
    raw = b"".join(
        b"\x00" + rgba[y * width * 4:(y + 1) * width * 4]
        for y in range(height)
    )

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + kind
            + payload
            + struct.pack(">I", binascii.crc32(kind + payload) & 0xFFFFFFFF)
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("roms", nargs="+", type=Path)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    image_dir = args.out / f"batch_{args.start:03d}_{args.end:03d}"
    image_dir.mkdir(parents=True, exist_ok=True)

    references: list[dict[str, object]] = []
    unique_assets: dict[tuple[int, str, str, str], dict[str, object]] = {}

    for rom_path in args.roms:
        data = rom_path.read_bytes()
        rom_sha1 = hashlib.sha1(data).hexdigest()
        picture_tables, palette_tables = find_sprite_tables(data)
        front_table, back_table = picture_tables
        normal_palette_table, shiny_palette_table = palette_tables

        for species in range(args.start, args.end + 1):
            front_ptr, _, _ = struct.unpack_from("<IHH", data, front_table + 8 * species)
            back_ptr, _, _ = struct.unpack_from("<IHH", data, back_table + 8 * species)
            normal_ptr, _, _ = struct.unpack_from("<IHH", data, normal_palette_table + 8 * species)
            shiny_ptr, _, _ = struct.unpack_from("<IHH", data, shiny_palette_table + 8 * species)

            front, front_stream_size = lz77_decompress_gba(data, front_ptr - ROM_BASE)
            back, back_stream_size = lz77_decompress_gba(data, back_ptr - ROM_BASE)
            normal, normal_stream_size = lz77_decompress_gba(data, normal_ptr - ROM_BASE)
            shiny, shiny_stream_size = lz77_decompress_gba(data, shiny_ptr - ROM_BASE)

            for pose, tile_data, pic_ptr, pic_stream_size in (
                ("front", front, front_ptr, front_stream_size),
                ("back", back, back_ptr, back_stream_size),
            ):
                tile_sha256 = hashlib.sha256(tile_data).hexdigest()
                for variant, palette_data, palette_ptr, palette_stream_size in (
                    ("normal", normal, normal_ptr, normal_stream_size),
                    ("shiny", shiny, shiny_ptr, shiny_stream_size),
                ):
                    palette_sha256 = hashlib.sha256(palette_data[:32]).hexdigest()
                    rgba = render_4bpp_64(tile_data, palette_data)
                    render_sha256 = hashlib.sha256(rgba).hexdigest()
                    key = (species, pose, variant, render_sha256)

                    if key not in unique_assets:
                        filename = (
                            f"{species:03d}_{pose}_{variant}_{render_sha256[:12]}.png"
                        )
                        png = png_bytes_rgba(64, 64, rgba)
                        (image_dir / filename).write_bytes(png)
                        unique_assets[key] = {
                            "species_id": species,
                            "pose": pose,
                            "variant": variant,
                            "render_sha256": render_sha256,
                            "tile_sha256": tile_sha256,
                            "palette_sha256": palette_sha256,
                            "asset_path": str((image_dir / filename).relative_to(args.out.parent)),
                            "source_count": 0,
                        }

                    unique_assets[key]["source_count"] = int(unique_assets[key]["source_count"]) + 1
                    references.append(
                        {
                            "rom_filename": rom_path.name,
                            "rom_sha1": rom_sha1,
                            "species_id": species,
                            "pose": pose,
                            "variant": variant,
                            "pic_pointer": f"0x{pic_ptr:08X}",
                            "pic_lz77_stream_bytes": pic_stream_size,
                            "tile_sha256": tile_sha256,
                            "palette_pointer": f"0x{palette_ptr:08X}",
                            "palette_lz77_stream_bytes": palette_stream_size,
                            "palette_sha256": palette_sha256,
                            "render_sha256": render_sha256,
                            "asset_path": unique_assets[key]["asset_path"],
                        }
                    )

    ref_path = args.out / f"batch_{args.start:03d}_{args.end:03d}_references.csv"
    unique_path = args.out / f"batch_{args.start:03d}_{args.end:03d}_unique.csv"

    with ref_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(references[0]))
        writer.writeheader()
        writer.writerows(references)

    uniques = sorted(
        unique_assets.values(),
        key=lambda row: (int(row["species_id"]), str(row["pose"]), str(row["variant"])),
    )
    with unique_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(uniques[0]))
        writer.writeheader()
        writer.writerows(uniques)

    print(f"references={len(references)} unique_assets={len(uniques)}")


if __name__ == "__main__":
    main()
