.section .rodata
names:
  .asciz "PTRACE_TRACEME"
  .asciz "PTRACE_PEEKTEXT"
  .asciz "PTRACE_PEEKDATA"
  .asciz "PTRACE_PEEKUSER"
  .asciz "PTRACE_POKETEXT"
  .asciz "PTRACE_POKEDATA"
  .asciz "PTRACE_POKEUSER"
  .asciz "PTRACE_CONT"
  .asciz "PTRACE_KILL"
  .asciz "PTRACE_SINGLESTEP"
  .asciz "PTRACE_GETREGS"
  .asciz "PTRACE_SETREGS"
  .asciz "PTRACE_GETFPREGS"
  .asciz "PTRACE_SETFPREGS"
  .asciz "PTRACE_ATTACH"
  .asciz "PTRACE_DETACH"
  .asciz "PTRACE_GETFPXREGS"
  .asciz "PTRACE_SETFPXREGS"
  .asciz "PTRACE_SYSCALL"
  .asciz "PTRACE_SETOPTIONS"
  .asciz "PTRACE_GETEVENTMSG"
.text
.globl main
.type main,@function
main:
  mov $101, %eax
  mov $4, %edi
  xor %esi, %esi
  xor %edx, %edx
  xor %r10d, %r10d
  syscall
  xor %eax, %eax
  ret
.size main, .-main
.section .note.GNU-stack,"",@progbits
