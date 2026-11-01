#!/usr/bin/env python3
"""Kullanim: dump.py prog.elf iz.txt.mem.json  -> global degiskenlerin adres/deger dokumu (1.5)"""
import sys, json, subprocess, re
elf, memf = sys.argv[1:3]
sym = {}
for l in subprocess.run(['llvm-objdump', '-t', elf], capture_output=True, text=True).stdout.splitlines():
    m = re.match(r'([0-9a-f]{8}) g\s+O\s+\S+\s+[0-9a-f]{8} (\S+)$', l)
    if m: sym[m[2]] = int(m[1], 16)
mem = {int(k): v for k, v in json.load(open(memf))['mem'].items()}
r = lambda a: sum(mem.get(a + i, 0) << (8 * i) for i in range(4))
print('program: %s' % elf)
print('checksum    @ %#010x = %#010x (%d)' % (sym['checksum'], r(sym['checksum']), r(sym['checksum'])))
print('decrypt_ok  @ %#010x = %d' % (sym['decrypt_ok'], r(sym['decrypt_ok'])))
for i in range(41):
    print('a[%2d]       @ %#010x = %3d (%s)' % (i, sym['a'] + 4 * i, r(sym['a'] + 4 * i), chr(r(sym['a'] + 4 * i))))
