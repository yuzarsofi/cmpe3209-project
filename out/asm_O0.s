	.text
	.attribute	4, 16
	.attribute	5, "rv32i2p1_m2p0"
	.file	"main.c"
	.globl	rotl                            # -- Begin function rotl
	.p2align	2
	.type	rotl,@function
rotl:                                   # @rotl
# %bb.0:
	addi	sp, sp, -16
	sw	ra, 12(sp)                      # 4-byte Folded Spill
	sw	s0, 8(sp)                       # 4-byte Folded Spill
	addi	s0, sp, 16
	sw	a0, -12(s0)
	lw	a0, -12(s0)
	srli	a1, a0, 31
	slli	a0, a0, 1
	or	a0, a0, a1
	lw	ra, 12(sp)                      # 4-byte Folded Reload
	lw	s0, 8(sp)                       # 4-byte Folded Reload
	addi	sp, sp, 16
	ret
.Lfunc_end0:
	.size	rotl, .Lfunc_end0-rotl
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	2
	.type	main,@function
main:                                   # @main
# %bb.0:
	addi	sp, sp, -48
	sw	ra, 44(sp)                      # 4-byte Folded Spill
	sw	s0, 40(sp)                      # 4-byte Folded Spill
	addi	s0, sp, 48
	li	a0, 0
	sw	a0, -12(s0)
	li	a0, 193
	sw	a0, -16(s0)
	lw	a0, -16(s0)
	bnez	a0, .LBB1_2
	j	.LBB1_1
.LBB1_1:
	li	a0, 165
	sw	a0, -16(s0)
	j	.LBB1_2
.LBB1_2:
	lui	a0, 300
	addi	a0, a0, 1217
	sw	a0, -20(s0)
	li	a0, 0
	sw	a0, -24(s0)
	j	.LBB1_3
.LBB1_3:                                # =>This Inner Loop Header: Depth=1
	lw	a1, -24(s0)
	li	a0, 40
	blt	a0, a1, .LBB1_6
	j	.LBB1_4
.LBB1_4:                                #   in Loop: Header=BB1_3 Depth=1
	lw	a0, -20(s0)
	lui	a1, 406
	addi	a1, a1, 1549
	mul	a0, a0, a1
	lui	a1, 247535
	addi	a1, a1, 863
	add	a0, a0, a1
	sw	a0, -20(s0)
	lw	a0, -20(s0)
	srli	a0, a0, 16
	lui	a1, 40330
	addi	a1, a1, -630
	mulhu	a1, a0, a1
	li	a2, 26
	mul	a1, a1, a2
	sub	a0, a0, a1
	addi	a0, a0, 65
	lw	a2, -24(s0)
	lui	a1, %hi(a)
	addi	a1, a1, %lo(a)
	slli	a2, a2, 2
	add	a1, a1, a2
	sw	a0, 0(a1)
	j	.LBB1_5
.LBB1_5:                                #   in Loop: Header=BB1_3 Depth=1
	lw	a0, -24(s0)
	addi	a0, a0, 1
	sw	a0, -24(s0)
	j	.LBB1_3
.LBB1_6:
	li	a0, 0
	sw	a0, -28(s0)
	j	.LBB1_7
.LBB1_7:                                # =>This Inner Loop Header: Depth=1
	lw	a1, -28(s0)
	li	a0, 40
	blt	a0, a1, .LBB1_10
	j	.LBB1_8
.LBB1_8:                                #   in Loop: Header=BB1_7 Depth=1
	lw	a0, -28(s0)
	slli	a1, a0, 2
	lui	a0, %hi(a)
	addi	a0, a0, %lo(a)
	sw	a0, -48(s0)                     # 4-byte Folded Spill
	add	a1, a0, a1
	lw	a0, 0(a1)
	lw	a2, -16(s0)
	xor	a0, a0, a2
	sw	a0, 0(a1)
	lui	a0, %hi(checksum)
	sw	a0, -44(s0)                     # 4-byte Folded Spill
	lw	a0, %lo(checksum)(a0)
	call	rotl
	lw	a2, -48(s0)                     # 4-byte Folded Reload
	lw	a1, -44(s0)                     # 4-byte Folded Reload
	lw	a3, -28(s0)
	slli	a3, a3, 2
	add	a2, a2, a3
	lw	a2, 0(a2)
	add	a0, a0, a2
	sw	a0, %lo(checksum)(a1)
	j	.LBB1_9
.LBB1_9:                                #   in Loop: Header=BB1_7 Depth=1
	lw	a0, -28(s0)
	addi	a0, a0, 1
	sw	a0, -28(s0)
	j	.LBB1_7
.LBB1_10:
	lui	a0, 300
	addi	a0, a0, 1217
	sw	a0, -20(s0)
	li	a0, 1
	sw	a0, -32(s0)
	li	a0, 0
	sw	a0, -36(s0)
	j	.LBB1_11
.LBB1_11:                               # =>This Inner Loop Header: Depth=1
	lw	a1, -36(s0)
	li	a0, 40
	blt	a0, a1, .LBB1_16
	j	.LBB1_12
.LBB1_12:                               #   in Loop: Header=BB1_11 Depth=1
	lw	a0, -20(s0)
	lui	a1, 406
	addi	a1, a1, 1549
	mul	a0, a0, a1
	lui	a1, 247535
	addi	a1, a1, 863
	add	a0, a0, a1
	sw	a0, -20(s0)
	lw	a0, -20(s0)
	srli	a0, a0, 16
	lui	a1, 40330
	addi	a1, a1, -630
	mulhu	a1, a0, a1
	li	a2, 26
	mul	a1, a1, a2
	sub	a0, a0, a1
	addi	a0, a0, 65
	sw	a0, -40(s0)
	lw	a1, -36(s0)
	lui	a0, %hi(a)
	addi	a0, a0, %lo(a)
	slli	a1, a1, 2
	add	a2, a0, a1
	lw	a1, 0(a2)
	lw	a3, -16(s0)
	xor	a1, a1, a3
	sw	a1, 0(a2)
	lw	a1, -36(s0)
	slli	a1, a1, 2
	add	a0, a0, a1
	lw	a0, 0(a0)
	lw	a1, -40(s0)
	beq	a0, a1, .LBB1_14
	j	.LBB1_13
.LBB1_13:                               #   in Loop: Header=BB1_11 Depth=1
	li	a0, 0
	sw	a0, -32(s0)
	j	.LBB1_14
.LBB1_14:                               #   in Loop: Header=BB1_11 Depth=1
	j	.LBB1_15
.LBB1_15:                               #   in Loop: Header=BB1_11 Depth=1
	lw	a0, -36(s0)
	addi	a0, a0, 1
	sw	a0, -36(s0)
	j	.LBB1_11
.LBB1_16:
	lw	a0, -32(s0)
	lui	a1, %hi(decrypt_ok)
	sw	a0, %lo(decrypt_ok)(a1)
	li	a0, 0
	lw	ra, 44(sp)                      # 4-byte Folded Reload
	lw	s0, 40(sp)                      # 4-byte Folded Reload
	addi	sp, sp, 48
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
	.addrsig_sym rotl
	.addrsig_sym checksum
	.addrsig_sym decrypt_ok
	.addrsig_sym a
