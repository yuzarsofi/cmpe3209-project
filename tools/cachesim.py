#!/usr/bin/env python3
"""Data cache simulatoru (Adim 4c-4g). Kullanim:
  cachesim.py trace.csv [--size 128] [--line 32] [--ways 1] [--policy wt|wb] [--detail 30] [--state-at 30]
  --ways 0 : fully associative.  Yer degistirme: LRU (direct mapping'de secim yok).
Adres alanlari (Stallings): word = log2(line), set/line = log2(set sayisi), tag = kalan ust bitler.
Write-through: her store bir ana bellek yazmasidir. Write-back: yalnizca dirty line cikarilirken (ve sonda kalan dirty line'lar) yazilir.
Write miss'te blok cache'e getirilir (write-allocate)."""
import sys, argparse, csv

def log2(x):
    n = 0
    while (1 << n) < x: n += 1
    assert (1 << n) == x, 'ikinin kuvveti olmali'
    return n

class Cache:
    def __init__(s, size, line, ways, policy):
        s.nlines = size // line
        s.ways = s.nlines if ways == 0 else ways
        s.nsets = s.nlines // s.ways
        s.w, s.d = log2(line), log2(s.nsets)
        s.policy = policy
        s.sets = [[] for _ in range(s.nsets)]   # her set: [tag, dirty] listesi; liste sonu = en son kullanilan (MRU)
        s.seen = set()                          # daha once cache'e girmis bloklar
        s.hit = s.miss = s.memw = s.memr = 0
    def fields(s, addr):
        word = addr & ((1 << s.w) - 1); st = (addr >> s.w) & (s.nsets - 1); tag = addr >> (s.w + s.d)
        return tag, st, word
    def access(s, rw, addr):
        tag, st, word = s.fields(addr); block = addr >> s.w
        S = s.sets[st]; ev = None; was = None
        ent = next((e for e in S if e[0] == tag), None)
        if ent:
            s.hit += 1; S.remove(ent); S.append(ent); res = 'Hit'
        else:
            s.miss += 1; s.memr += 1; res = 'Miss'; was = block in s.seen
            if len(S) == s.ways:
                old = S.pop(0); ev = (old[0] << s.d | st) << s.w   # cikan blogun baslangic adresi
                if old[1] and s.policy == 'wb': s.memw += 1
            ent = [tag, False]; S.append(ent); s.seen.add(block)
        if rw == 'W':
            if s.policy == 'wt': s.memw += 1
            else: ent[1] = True
        return tag, st, word, res, ev, was
    def flush_count(s):
        return sum(1 for S in s.sets for e in S if e[1])
    def state(s):
        rows = []
        for i, S in enumerate(s.sets):
            for j in range(s.ways):
                if j < len(S):
                    e = S[j]; rows.append((i, j, 1, e[0], int(e[1]), len(S) - 1 - j))  # LRU sirasi: 0 = en son kullanilan
                else: rows.append((i, j, 0, None, 0, None))
        return rows

def read_trace(path):
    with open(path) as f:
        return [(r['RW'], int(r['adres_hex'], 16)) for r in csv.DictReader(f)]

def run(trace, size, line, ways, policy, detail=0, state_at=0, out=sys.stdout):
    c = Cache(size, line, ways, policy)
    if detail:
        out.write('cache: %d B, line %d B, %s, %d line, %d set; alanlar: tag %d bit, %s %d bit, word %d bit; policy %s\n' % (
            size, line, 'direct' if c.ways == 1 else ('fully associative' if c.nsets == 1 else '%d-way' % c.ways), c.nlines, c.nsets,
            32 - c.w - c.d, 'line' if c.ways == 1 else 'set', c.d, c.w, 'write-through' if policy == 'wt' else 'write-back'))
        out.write('%3s %2s %-10s %-9s %4s %4s %-4s %-12s %s\n' % ('#', 'RW', 'adres', 'tag', 'line', 'word', 'sonuc', 'cikan blok', 'daha once cachete miydi'))
    for i, (rw, ad) in enumerate(trace, 1):
        tag, st, word, res, ev, was = c.access(rw, ad)
        if i <= detail:
            out.write('%3d %2s 0x%08x 0x%07x %4d %4d %-4s %-12s %s\n' % (i, rw, ad, tag, st, word, res, ('0x%08x' % ev) if ev is not None else '-', '-' if was is None else ('evet' if was else 'hayir')))
        if i == state_at:
            out.write('--- %d. referanstan sonra cache ani (hit %d, miss %d, bellege yazma %d) ---\n' % (i, c.hit, c.miss, c.memw))
            for (s_, j, v, t, d, l) in c.state():
                out.write('set/line %d way %d: valid %d tag %s dirty %d lru %s\n' % (s_, j, v, ('0x%07x' % t) if t is not None else '-', d, '-' if l is None else l))
    left = c.flush_count()
    return dict(ref=len(trace), hit=c.hit, miss=c.miss, H=c.hit / len(trace), memw=c.memw, kalan_dirty=left)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('trace'); ap.add_argument('--size', type=int, default=128); ap.add_argument('--line', type=int, default=32)
    ap.add_argument('--ways', type=int, default=1); ap.add_argument('--policy', default='wt'); ap.add_argument('--detail', type=int, default=0)
    ap.add_argument('--state-at', type=int, default=0)
    a = ap.parse_args()
    r = run(read_trace(a.trace), a.size, a.line, a.ways, a.policy, a.detail, a.state_at)
    print('toplam: referans %(ref)d, hit %(hit)d, miss %(miss)d, H = %(H).4f, ana bellege yazma %(memw)d, sonda kalan dirty line %(kalan_dirty)d' % r)

if __name__ == '__main__':
    main()
