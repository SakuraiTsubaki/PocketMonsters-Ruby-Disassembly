# Japanese Thumb entry reachable disassembly

Starting at the proven Thumb transition target `0x0800024c`, conservative control-flow traversal records 107 reachable halfwords, 18 direct CFG edges, and 21 BL call sites. BL targets are recorded without following callees, and unreachable gaps are represented by explicit `.org` directives in the source.

The source halfwords in ascending address order have canonical SHA-256 `a45d324ca50899ec4d18e953379a8463c4f1710a240ac89fabb5dd857a33bd36`. No return is reachable in this graph, so this is documented as a non-returning bootstrap path rather than a complete function boundary. Every emitted `.hword` is checked against its original little-endian ROM bytes.

