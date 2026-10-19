.text
.globl _main
_main:
 strb wzr, [x21, w25, sxtw]
 mov x27, x0
 mov x0, x21
 bl hash_name
 mov x8, x0
 mov x0, x27
 cmp x8, x22
 b.ne done
 str x26, [sp, #0x20]
 add x0, sp, #0x20
 mov x1, x20
 bl read_uleb
 ldr x8, [sp, #0x20]
 cmp x8, x20
 b.hi done
 mov w8, #0x1b
 and x8, x0, x8
 cbnz x8, done
 add x0, sp, #0x20
 mov x1, x20
 bl read_uleb
 ldr x8, [sp, #0x20]
 cmp x8, x20
 b.hi done
 add x0, x0, x19
done:
 ret
hash_name:
 ret
read_uleb:
 ret
