.text
.globl _main
_main:
 mov w12, #0x5678
 movk w12, #0x1234, lsl #16
 eor w12, w19, w12
 sub x9, x0, x22
 mov w10, #0x10
 movk w10, #0x2fa, lsl #16
 cmp x9, x10
 csel w12, w12, w19, hi
 rev w12, w12
 str w12, [sp, #0x10]
 ret
