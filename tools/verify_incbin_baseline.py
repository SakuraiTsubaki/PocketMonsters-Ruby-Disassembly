#!/usr/bin/env python3
"""Build a byte-preserving ROM baseline from a local baserom via .incbin.

The baserom remains local and is never copied into repository artifacts.
Requires clang with ARM target support and ld.lld.
"""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, tempfile

def q(s: str) -> str:
    return s.replace('\\','\\\\').replace('"','\\"')

def build_one(rom: Path, output: Path):
    clang=shutil.which('clang') or '/usr/local/swift/usr/bin/clang'
    lld=shutil.which('ld.lld') or '/usr/local/swift/usr/bin/ld.lld'
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        asm=td/'baseline.s'; obj=td/'baseline.o'; ld=td/'rom.ld'
        asm.write_text('.syntax unified\n.cpu arm7tdmi\n.section .rom,"a",%progbits\n.global rom_start\nrom_start:\n.incbin "'+q(str(rom.resolve()))+'"\n')
        ld.write_text('SECTIONS { . = 0x08000000; .rom : { KEEP(*(.rom)) } }\n')
        subprocess.run([clang,'--target=armv4t-none-eabi','-c',str(asm),'-o',str(obj)],check=True)
        subprocess.run([lld,'-T',str(ld),'--oformat=binary',str(obj),'-o',str(output)],check=True)

def sha256(p: Path): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('roms',nargs='+',type=Path); ap.add_argument('--out-dir',type=Path); args=ap.parse_args()
    out_dir=args.out_dir or Path.cwd()/'baseline-out'; out_dir.mkdir(parents=True,exist_ok=True)
    result=[]
    for rom in args.roms:
        built=out_dir/(rom.stem+'.baseline.gba'); build_one(rom,built)
        a,b=sha256(rom),sha256(built)
        result.append({'file':rom.name,'source_sha256':a,'baseline_sha256':b,'match':a==b,'size_bytes':rom.stat().st_size})
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if all(x['match'] for x in result) else 1)
if __name__=='__main__': main()
