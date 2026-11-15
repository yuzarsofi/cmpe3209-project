#!/usr/bin/env python3
"""Adim 4d-4f: tam simulasyon, tasarim uzayi (4e) ve grafik. Kullanim: sweep.py trace.csv grafik.png [T1 T2]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cachesim import run, read_trace

def main():
    tr = read_trace(sys.argv[1]); png = sys.argv[2]
    T1 = int(sys.argv[3]) if len(sys.argv) > 3 else 1; T2 = int(sys.argv[4]) if len(sys.argv) > 4 else 35
    base = run(tr, 128, 32, 1, 'wt')
    print('kisiye ozel cache (128 B, 32 B line, direct, write-through): ref %(ref)d hit %(hit)d miss %(miss)d H %(H).4f bellege yazma %(memw)d' % base)
    wb = run(tr, 128, 32, 1, 'wb')
    print('karsilastirma, write-back olsaydi: bellege yazma %d (+ sonda kalan dirty line %d)' % (wb['memw'], wb['kalan_dirty']))
    Ts = base['H'] * T1 + (1 - base['H']) * (T1 + T2)
    print('T_s = H*T1 + (1-H)*(T1+T2) = %.4f cycle; cache yok: %d cycle; speedup %.3f' % (Ts, T2, T2 / Ts))
    print('\n4e mapping serisi (line 32 B):')
    maps = [('Direct', 1), ('2-way', 2), ('4-way', 4), ('Fully assoc. (LRU)', 0)]
    hm = []
    for name, w in maps:
        r = run(tr, 128, 32, w, 'wt'); hm.append(r['H'])
        print('  %-20s hit %4d miss %4d H %.4f' % (name, r['hit'], r['miss'], r['H']))
    print('4e line boyu serisi (direct):')
    lines = [8, 16, 32, 64]; hl = []
    for ln in lines:
        r = run(tr, 128, ln, 1, 'wt'); hl.append(r['H'])
        print('  %2d B (%2d line)       hit %4d miss %4d H %.4f' % (ln, 128 // ln, r['hit'], r['miss'], r['H']))
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib yok, grafik cizilmedi'); return
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    ax[0].bar([m[0] for m in maps], hm, color='#4c6a8a'); ax[0].set_title('Mapping (cache 128 B, line 32 B)'); ax[0].set_ylabel('Hit ratio H')
    ax[1].plot([str(l) for l in lines], hl, marker='o', color='#4c6a8a'); ax[1].set_title('Line boyu (cache 128 B, direct)'); ax[1].set_xlabel('Line boyu (byte)')
    lo = min(hm + hl) - 0.03
    for a, vals in ((ax[0], hm), (ax[1], hl)):
        a.set_ylim(lo, 1.0)
        for i, v in enumerate(vals): a.annotate('%.4f' % v, (i, v), textcoords='offset points', xytext=(0, 5), ha='center', fontsize=8)
    ax[0].tick_params(axis='x', labelsize=8)
    fig.tight_layout(); fig.savefig(png, dpi=150)

if __name__ == '__main__':
    main()
