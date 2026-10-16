.section .text,"awx"
.globl _entry
_entry:
.rept 65536
.byte 0
.endr
.byte 0xc3
