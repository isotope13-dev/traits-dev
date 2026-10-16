.section .text
.globl _start
_start:
.rept 128
.byte 0
.endr
.byte 0xc3
