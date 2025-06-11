.globl gcd
.globl main
.data
.text
gcd:
	addiu $sp, $sp, -8
	sw $ra, 4($sp)
	sw $fp, 0($sp)
	addiu $fp, $sp, 0
	lw $t0, 12($fp)
	addiu $sp, $sp, -4
	sw $t0, 0($sp)
	li $t0, 0
	lw $t1, 0($sp)
	addiu $sp, $sp, 4
	xor $t0, $t0, $t1
	sltu $t0, $t0, 1
	beqz $t0, else_1992613408896
	lw $t0, 8($fp)
	move $v0, $t0
	j gcd_epilogue
	j endif_1992613408896
else_1992613408896:
	lw $t0, 8($fp)
	addiu $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 8($fp)
	addiu $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 12($fp)
	lw $t1, 0($sp)
	addiu $sp, $sp, 4
	div $t1, $t0
	mflo $t0
	addiu $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 12($fp)
	lw $t1, 0($sp)
	addiu $sp, $sp, 4
	mul $t0, $t1, $t0
	lw $t1, 0($sp)
	addiu $sp, $sp, 4
	sub $t0, $t1, $t0
	addiu $sp, $sp, -4
	sw   $t0, 0($sp)
	lw $t0, 12($fp)
	addiu $sp, $sp, -4
	sw   $t0, 0($sp)
	jal gcd
	addiu $sp, $sp, 8
	move $t0, $v0
	move $v0, $t0
	j gcd_epilogue
endif_1992613408896:
gcd_epilogue:
	lw $ra, 4($fp)
	lw $fp, 0($fp)
	addiu $sp, $sp, 8
	jr $ra

main:
	addiu $sp, $sp, -20
	sw $ra, 16($sp)
	sw $fp, 12($sp)
	addiu $fp, $sp, 12
	li $v0, 5
	syscall
	move $t0, $v0
	sw $t0, -4($fp)
	li $v0, 5
	syscall
	move $t0, $v0
	sw $t0, -8($fp)
	lw $t0, -8($fp)
	addiu $sp, $sp, -4
	sw   $t0, 0($sp)
	lw $t0, -4($fp)
	addiu $sp, $sp, -4
	sw   $t0, 0($sp)
	jal gcd
	addiu $sp, $sp, 8
	move $t0, $v0
	move $a0, $t0
	li $v0, 1
	syscall
	li $a0, 10
	li $v0, 11
	syscall
	move $t0, $zero
main_epilogue:
	lw $ra, 4($fp)
	lw $fp, 0($fp)
	addiu $sp, $sp, 20
	jr $ra

main_exit:
	li $v0, 10
	syscall
