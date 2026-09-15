#!/usr/bin/env python3
"""Inventory Pokémon Ruby GBA ROMs without modifying or redistributing them."""
from pathlib import Path
import argparse, hashlib, json, struct

def header(data: bytes):
    inst=struct.unpack_from('<I',data,0)[0]
    imm=inst & 0xFFFFFF
    if imm & 0x800000: imm -= 0x1000000
    entry=0x08000008 + imm*4
    calc=(-sum(data[0xA0:0xBD])-0x19) & 0xFF
    return {
        'title': data[0xA0:0xAC].rstrip(b'\0').decode('ascii','replace'),
        'game_code': data[0xAC:0xB0].decode('ascii','replace'),
        'maker_code': data[0xB0:0xB2].decode('ascii','replace'),
        'software_version': data[0xBC],
        'complement_check': data[0xBD],
        'computed_complement_check': calc,
        'header_checksum_valid': calc == data[0xBD],
        'entry_target': f'0x{entry:08X}',
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('roms', nargs='+', type=Path); args=ap.parse_args()
    result=[]
    for p in args.roms:
        b=p.read_bytes()
        result.append({'file':p.name,'size_bytes':len(b),'md5':hashlib.md5(b).hexdigest(),'sha1':hashlib.sha1(b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),'header':header(b)})
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
