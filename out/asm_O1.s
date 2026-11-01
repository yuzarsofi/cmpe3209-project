	.text
	.attribute	4, 16
	.attribute	5, "rv32i2p1_m2p0"
	.file	"main.c"
	.globl	rotl                            # -- Begin function rotl
	.p2align	2
	.type	rotl,@function
rotl:                                   # @rotl
# %bb.0:
	srli	a1, a0, 31
	slli	a0, a0, 1
	or	a0, a0, a1
	ret
.Lfunc_end0:
	.size	rotl, .Lfunc_end0-rotl
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	2
	.type	main,@function
main:                                   # @main
# %bb.0:
	lui	a0, 247535
	addi	a0, a0, 863
	lui	a1, %hi(a)
	addi	a2, a1, %lo(a)
	lui	a1, 300
	addi	a3, a1, 1217
	lui	a1, 406
	addi	a1, a1, 1549
	lui	a4, 40330
	addi	a4, a4, -630
	li	a5, 26
	addi	a6, a2, 164
.LBB1_1:                                # =>This Inner Loop Header: Depth=1
	mul	a3, a3, a1
	add	a3, a3, a0
	srli	a7, a3, 16
	mulhu	t0, a7, a4
	mul	t0, t0, a5
	sub	a7, a7, t0
	addi	a7, a7, 65
	sw	a7, 0(a2)
	addi	a2, a2, 4
	bne	a2, a6, .LBB1_1
# %bb.2:
	lui	a2, %hi(checksum)
	lw	a2, %lo(checksum)(a2)
	lui	a3, %hi(a)
	addi	a3, a3, %lo(a)
	addi	a4, a3, 164
.LBB1_3:                                # =>This Inner Loop Header: Depth=1
	lw	a5, 0(a3)
	xori	a5, a5, 193
	sw	a5, 0(a3)
	srli	a6, a2, 31
	slli	a2, a2, 1
	or	a2, a2, a6
	addi	a3, a3, 4
	add	a2, a2, a5
	bne	a3, a4, .LBB1_3
# %bb.4:
	lui	a3, %hi(checksum)
	sw	a2, %lo(checksum)(a3)
	lui	a2, %hi(a)
	addi	a3, a2, %lo(a)
	li	a2, 1
	lui	a4, 300
	addi	a4, a4, 1217
	lui	a5, 40330
	addi	a5, a5, -630
	li	a6, 26
	addi	a7, a3, 164
.LBB1_5:                                # =>This Inner Loop Header: Depth=1
	mul	a4, a4, a1
	add	a4, a4, a0
	srli	t0, a4, 16
	mulhu	t1, t0, a5
	lw	t2, 0(a3)
	mul	t1, t1, a6
	sub	t0, t0, t1
	addi	t0, t0, 65
	xori	t1, t2, 193
	sw	t1, 0(a3)
	xor	t0, t1, t0
	snez	t0, t0
	addi	t0, t0, -1
	addi	a3, a3, 4
	and	a2, t0, a2
	bne	a3, a7, .LBB1_5
# %bb.6:
	lui	a0, %hi(decrypt_ok)
	sw	a2, %lo(decrypt_ok)(a0)
	li	a0, 0
	ret
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
                                        # -- End function
	.type	SID,@object                     # @SID
	.section	.rodata,"a",@progbits
	.globl	SID
	.p2align	2, 0x0
SID:
	.word	1230017                         # 0x12c4c1
	.size	SID, 4

	.type	checksum,@object                # @checksum
	.section	.sbss,"aw",@nobits
	.globl	checksum
	.p2align	2, 0x0
checksum:
	.word	0                               # 0x0
	.size	checksum, 4

	.type	decrypt_ok,@object              # @decrypt_ok
	.globl	decrypt_ok
	.p2align	2, 0x0
decrypt_ok:
	.word	0                               # 0x0
	.size	decrypt_ok, 4

	.type	a,@object                       # @a
	.bss
	.globl	a
	.p2align	2, 0x0
a:
	.zero	164
	.size	a, 164

	.ident	"Ubuntu clang version 18.1.3 (1ubuntu1)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
