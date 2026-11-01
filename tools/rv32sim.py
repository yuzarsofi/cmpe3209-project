#!/usr/bin/env python3
"""Minimal RV32IM yorumlayici (CMPE3209 M1). Kullanim: rv32sim.py prog.elf objdump.txt iz.txt
ELF yukler, main'den baslar, ra=0'a donunce durur; dinamik instruction izini yazar."""
import struct, sys, re
M = 0xFFFFFFFF
def sx(v, b): return v - (1 << b) if v & (1 << (b - 1)) else v

def load_elf(path):
    d = open(path, 'rb').read()
    entry = struct.unpack_from('<I', d, 24)[0]
    phoff, = struct.unpack_from('<I', d, 28); phentsize, phnum = struct.unpack_from('<HH', d, 42)
    mem = {}
    for i in range(phnum):
        t, off, va, pa, fsz, msz, fl, al = struct.unpack_from('<8I', d, phoff + i * phentsize)
        if t != 1: continue
        for j in range(fsz): mem[va + j] = d[off + j]
        for j in range(fsz, msz): mem[va + j] = 0
    return entry, mem

class CPU:
    def __init__(s, entry, mem):
        s.pc, s.mem, s.x = entry, mem, [0] * 32
        s.x[2] = 0x7FFF0000; s.x[1] = 0
        s.n = 0
    def r32(s, a): return sum(s.mem.get(a + i, 0) << (8 * i) for i in range(4))
    def w32(s, a, v):
        for i in range(4): s.mem[a + i] = (v >> (8 * i)) & 255
    def step(s):
        pc = s.pc; w = s.r32(pc); op = w & 0x7F
        rd = (w >> 7) & 31; f3 = (w >> 12) & 7; rs1 = (w >> 15) & 31; rs2 = (w >> 20) & 31; f7 = w >> 25
        x = s.x; a, b = x[rs1], x[rs2]; npc = pc + 4; res = None
        if op == 0x37: res = w & 0xFFFFF000
        elif op == 0x17: res = (pc + (w & 0xFFFFF000)) & M
        elif op == 0x6F:
            imm = sx(((w >> 31) << 20) | (((w >> 12) & 0xFF) << 12) | (((w >> 20) & 1) << 11) | (((w >> 21) & 0x3FF) << 1), 21)
            res = pc + 4; npc = (pc + imm) & M
        elif op == 0x67:
            imm = sx(w >> 20, 12); res = pc + 4; npc = (a + imm) & ~1 & M
        elif op == 0x63:
            imm = sx(((w >> 31) << 12) | (((w >> 7) & 1) << 11) | (((w >> 25) & 0x3F) << 5) | (((w >> 8) & 0xF) << 1), 13)
            sa, sb = sx(a, 32), sx(b, 32)
            t = {0: a == b, 1: a != b, 4: sa < sb, 5: sa >= sb, 6: a < b, 7: a >= b}[f3]
            if t: npc = (pc + imm) & M
        elif op == 0x03:
            ad = (a + sx(w >> 20, 12)) & M
            if f3 == 2: res = s.r32(ad)
            elif f3 == 0: res = sx(s.mem.get(ad, 0), 8) & M
            elif f3 == 4: res = s.mem.get(ad, 0)
            elif f3 == 1: res = sx(s.mem.get(ad, 0) | s.mem.get(ad + 1, 0) << 8, 16) & M
            elif f3 == 5: res = s.mem.get(ad, 0) | s.mem.get(ad + 1, 0) << 8
            else: raise Exception('lw?')
        elif op == 0x23:
            ad = (a + sx(((w >> 25) << 5) | ((w >> 7) & 31), 12)) & M
            if f3 == 2: s.w32(ad, b)
            elif f3 == 0: s.mem[ad] = b & 255
            elif f3 == 1: s.mem[ad] = b & 255; s.mem[ad + 1] = (b >> 8) & 255
        elif op in (0x13, 0x33):
            if op == 0x13:
                imm = sx(w >> 20, 12); bb = imm & M; sh = rs2
            else: bb = b; sh = b & 31
            alt = f7 == 0x20
            if op == 0x33 and f7 == 1:
                sa, sb = sx(a, 32), sx(b, 32)
                if f3 == 0: res = (a * b) & M
                elif f3 == 1: res = ((sa * sb) >> 32) & M
                elif f3 == 2: res = ((sa * b) >> 32) & M
                elif f3 == 3: res = ((a * b) >> 32) & M
                elif f3 == 4: res = M if b == 0 else (abs(sa) // abs(sb) * (1 if (sa < 0) == (sb < 0) else -1)) & M
                elif f3 == 5: res = M if b == 0 else a // b
                elif f3 == 6: res = a if b == 0 else (sa - sx(((abs(sa) // abs(sb)) * (1 if (sa < 0) == (sb < 0) else -1)) & M, 32) * sb) & M
                else: res = a if b == 0 else a % b
            elif f3 == 0: res = (a - bb) & M if (op == 0x33 and alt) else (a + bb) & M
            elif f3 == 1: res = (a << sh) & M
            elif f3 == 2: res = int(sx(a, 32) < sx(bb, 32))
            elif f3 == 3: res = int(a < bb)
            elif f3 == 4: res = a ^ bb
            elif f3 == 5: res = (sx(a, 32) >> sh) & M if alt else a >> sh
            elif f3 == 6: res = a | bb
            else: res = a & bb
        else: raise Exception('bilinmeyen opcode %#x pc=%#x' % (op, pc))
        if res is not None and rd: x[rd] = res & M
        s.pc = npc; s.n += 1
        return pc, w

def main():
    elf, dump, out = sys.argv[1:4]
    asm = {}
    for l in open(dump):
        m = re.match(r'\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} ){4})\s*(.*)', l)
        if m: asm[int(m[1], 16)] = m[3].strip()
    e, mem = load_elf(elf); c = CPU(e, mem)
    with open(out, 'w') as f:
        f.write('# dinamik instruction izi: sira  pc  makine_kodu  assembly\n')
        while c.pc != 0 and c.n < 5_000_000:
            pc, w = c.step()
            f.write('%d\t%#x\t%08x\t%s\n' % (c.n, pc, w, asm.get(pc, '?')))
    print('dinamik instruction sayisi (Ic):', c.n)
    import json; json.dump({'mem': {str(k): v for k, v in c.mem.items() if k >= 0x12000 and k < 0x13000}}, open(out + '.mem.json', 'w'))
main()
