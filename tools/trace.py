#!/usr/bin/env python3
"""Data adres izi (Adim 4a) ve dinamik instruction siniflari (Adim 5a).
Kullanim: trace.py prog.elf prog_g.elf trace.csv
  prog.elf   : calistirilan program (rv32sim ile ayni yorumlayici)
  prog_g.elf : ayni kodun -g ile derlenmis hali; yalnizca adres -> C satiri eslemesi icin (yoksa '-' yazin)
Cikti CSV: sira,RW,adres_hex,boyut,c_satiri,stack_mi   (stack_mi: adres >= 0x7ffe0000 ise 1)
Ozet (stdout): Ic, sinif sayilari, satir bazinda instruction/referans sayilari."""
import sys, re, subprocess, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv32sim import CPU, load_elf, sx, M

def line_map(gelf):
    """llvm-dwarfdump satir tablosundan adres -> C satiri. Satir 0 kayitlari sonraki gercek satira baglanir."""
    if gelf == '-': return {}
    rows = []
    for l in subprocess.run(['llvm-dwarfdump', '--debug-line', gelf], capture_output=True, text=True).stdout.splitlines():
        m = re.match(r'0x([0-9a-f]+)\s+(\d+)\s', l)
        if m: rows.append((int(m[1], 16), int(m[2])))
    rows.sort()
    dis = {}
    for l in subprocess.run(['llvm-objdump', '-d', '--no-show-raw-insn', gelf], capture_output=True, text=True).stdout.splitlines():
        m = re.match(r'\s*([0-9a-f]+):\s+(\S+)', l)
        if m: dis[int(m[1], 16)] = m[2]
    lo = {}
    for a in sorted(dis):
        prev = [r for r in rows if r[0] <= a]; cur = prev[-1][1] if prev else 0
        if cur == 0:
            nxt = [r for r in rows if r[0] > a and r[1] != 0]; cur = nxt[0][1] if nxt else 0
        lo[a] = cur
    starts = {r[0] for r in rows}
    for a in sorted(dis):  # bir sonraki satirin sabit yuklemesi (li) onceki satira yazilmissa duzelt
        if dis[a] == 'li' and (a + 4) in starts and lo.get(a + 4, 0) not in (0, lo[a]): lo[a] = lo[a + 4]
    return lo

def klass(w):
    op = w & 0x7F
    if op == 0x03: return 'load'
    if op == 0x23: return 'store'
    if op in (0x63, 0x6F, 0x67): return 'branch'
    if op == 0x33 and (w >> 25) == 1: return 'mul'
    return 'alu'

def main():
    elf, gelf, out = sys.argv[1:4]
    lo = line_map(gelf)
    e, mem = load_elf(elf); c = CPU(e, mem)
    cls = {'alu': 0, 'mul': 0, 'load': 0, 'store': 0, 'branch': 0}
    per_line = {}  # satir -> [instr, load, store, mul, branch]
    n = 0
    with open(out, 'w') as f:
        f.write('sira,RW,adres_hex,boyut,c_satiri,stack_mi\n')
        while c.pc != 0 and c.n < 5_000_000:
            pc = c.pc; w = c.r32(pc); op = w & 0x7F; f3 = (w >> 12) & 7
            k = klass(w); cls[k] += 1
            ln = lo.get(pc, 0)
            pl = per_line.setdefault(ln, {'instr': 0, 'alu': 0, 'mul': 0, 'load': 0, 'store': 0, 'branch': 0})
            pl['instr'] += 1; pl[k] += 1
            if op in (0x03, 0x23):
                base = c.x[(w >> 15) & 31]
                imm = sx(w >> 20, 12) if op == 0x03 else sx(((w >> 25) << 5) | ((w >> 7) & 31), 12)
                ad = (base + imm) & M
                size = {0: 1, 1: 2, 2: 4, 4: 1, 5: 2}[f3]
                n += 1
                f.write('%d,%s,0x%08x,%d,%s,%d\n' % (n, 'R' if op == 0x03 else 'W', ad, size, ln if ln else '', int(ad >= 0x7FFE0000)))
            c.step()
    print(json.dumps({'Ic': c.n, 'siniflar': cls, 'data_ref': n, 'satir': {str(k): v for k, v in sorted(per_line.items())}}, indent=1))

if __name__ == '__main__':
    main()
