from pathlib import Path
import struct, sys
src=Path(sys.argv[1]); out=Path(sys.argv[2]); fileoff=int(sys.argv[3],0); base=int(sys.argv[4],0); size=int(sys.argv[5],0)
data=src.read_bytes()[fileoff:fileoff+size]
e_ident=b'\x7fELF'+bytes([1,1,1,0])+bytes(8)
EH=52; SH=40
shstr=b'\x00.text\x00.shstrtab\x00'
text_off=0x100
shstr_off=(text_off+len(data)+3)&~3
shoff=(shstr_off+len(shstr)+3)&~3
hdr=struct.pack('<16sHHIIIIIHHHHHH',e_ident,2,40,1,base,0,shoff,0x05000000,EH,0,0,SH,3,2)
sh0=bytes(SH)
sh1=struct.pack('<IIIIIIIIII',1,1,0x6,base,text_off,len(data),0,0,2,0)
sh2=struct.pack('<IIIIIIIIII',7,3,0,0,shstr_off,len(shstr),0,0,1,0)
blob=bytearray(hdr); blob.extend(bytes(text_off-len(blob))); blob.extend(data); blob.extend(bytes(shstr_off-len(blob))); blob.extend(shstr); blob.extend(bytes(shoff-len(blob))); blob.extend(sh0+sh1+sh2); out.write_bytes(blob)
