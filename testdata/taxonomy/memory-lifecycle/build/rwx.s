.global entry
.text
entry:
 mov $9, %rax
 xor %rdi, %rdi
 mov $4096, %rsi
 mov $6, %rdx
 mov $34, %r10
 mov $-1, %r8
 xor %r9,%r9
 syscall
 ret
