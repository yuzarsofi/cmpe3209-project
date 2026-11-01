# CMPE3209 proje (G3, RV32IM)

Depo: https://github.com/yuzarsofi/cmpe3209-project (etiket: M1)

- main.c: C programi (SID 5001230017, programda son 9 hane 1230017)
- out/asm_O0.s, out/asm_O1.s, out/objdump_O0.txt, out/objdump_O1.txt: derleme ciktilari
- out/iz_O0.txt, out/iz_O1.txt: dinamik instruction izi; out/bellek_*.txt: bellek dokumu
- tools/rv32sim.py, tools/dump.py: RV32IM yorumlayici ve bellek dokumu

Derleme: clang --target=riscv32 -march=rv32im -mabi=ilp32 -O0 -c main.c ; ld.lld -m elf32lriscv -e main main.o -o main.elf
Calistirma: python3 tools/rv32sim.py main.elf objdump.txt iz.txt
