# CMPE3209 proje (G3, RV32IM)

Depo: https://github.com/yuzarsofi/cmpe3209-project (etiket: M1)

- main.c: C programi (SID 5001230017, programda son 9 hane 1230017)
- out/asm_O0.s, out/asm_O1.s, out/objdump_O0.txt, out/objdump_O1.txt: derleme ciktilari
- out/iz_O0.txt, out/iz_O1.txt: dinamik instruction izi; out/bellek_*.txt: bellek dokumu
- tools/rv32sim.py, tools/dump.py: RV32IM yorumlayici ve bellek dokumu

Derleme: clang --target=riscv32 -march=rv32im -mabi=ilp32 -O0 -c main.c ; ld.lld -m elf32lriscv -e main main.o -o main.elf
Calistirma: python3 tools/rv32sim.py main.elf objdump.txt iz.txt

Final paketi (Adim 3-5):
- main_v2.c: Adim 4g surumu (tek degisiklik: satir 27-29, a[i] ^ K yerel degiskende tutulur); out/main_v2_O0.elf, out/objdump_v2_O0.txt, out/bellek_v2_O0.txt
- out/trace.csv (-O0), out/trace_O1.csv, out/trace_v2.csv: data adres izi (sira,RW,adres_hex,boyut,c_satiri,stack_mi)
- out/ozet_*.json: Ic, instruction siniflari ve C satiri bazinda sayimlar
- out/cache_sim.txt: ilk 30 referans ve cache ani; out/cache_sonuc*.txt: tam simulasyon ve tasarim uzayi; out/grafik_4e.png
- tools/trace.py (iz), tools/cachesim.py (cache simulatoru), tools/sweep.py (4d-4f ve grafik)
- out/*_g.elf: ayni kodun -g ile derlenmis hali (yalnizca adres -> C satiri eslemesi icin)

Iz: python3 tools/trace.py out/main_O0.elf out/main_O0_g.elf out/trace.csv
Cache: python3 tools/cachesim.py out/trace.csv --size 128 --line 32 --ways 1 --policy wt --detail 30 --state-at 30
Tasarim uzayi: python3 tools/sweep.py out/trace.csv out/grafik_4e.png 1 35
