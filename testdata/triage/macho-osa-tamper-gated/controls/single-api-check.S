.text
.globl _main
_main:
 mov w10, #0x50
 movk w10, #0x5800, lsl #16
 ldr w12, [x8]
 cmp w12, w10
 b.eq hit
 mov w11, #0xd4200000
 and w12, w12, #0xffe0001f
 cmp w12, w11
 b.eq hit
 nop
 cmp w12, w10
 b.eq hit
 and w10, w12, #0xffe0001f
 cmp w10, w11
 b.ne done
hit:
 mov x8, #0
 str xzr, [x26, #0x80]
done:
 ret
