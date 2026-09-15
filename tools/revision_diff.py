#!/usr/bin/env python3
"""Byte-compare two equal-size ROMs and report contiguous changed ranges."""
from pathlib import Path
import argparse, json

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('old',type=Path); ap.add_argument('new',type=Path); args=ap.parse_args()
    a=args.old.read_bytes(); b=args.new.read_bytes()
    if len(a)!=len(b): raise SystemExit('ROM sizes differ')
    changed=[]; runs=[]; start=prev=None
    for i,(x,y) in enumerate(zip(a,b)):
        if x!=y:
            changed.append(i)
            if start is None: start=prev=i
            elif i==prev+1: prev=i
            else: runs.append((start,prev)); start=prev=i
    if start is not None: runs.append((start,prev))
    print(json.dumps({'different_bytes':len(changed),'runs':[{'start':f'0x{s:X}','end':f'0x{e:X}','length':e-s+1} for s,e in runs]},indent=2))
if __name__=='__main__': main()
