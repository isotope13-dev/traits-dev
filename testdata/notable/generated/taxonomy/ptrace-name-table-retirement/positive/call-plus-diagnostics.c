#include <stdio.h>
#include <sys/ptrace.h>
int main(int argc, char **argv) {
  puts("PTRACE_TRACEME");
  puts("PTRACE_PEEKTEXT");
  puts("PTRACE_PEEKDATA");
  puts("PTRACE_PEEKUSER");
  puts("PTRACE_POKETEXT");
  puts("PTRACE_POKEDATA");
  puts("PTRACE_POKEUSER");
  puts("PTRACE_CONT");
  puts("PTRACE_KILL");
  puts("PTRACE_SINGLESTEP");
  puts("PTRACE_GETREGS");
  puts("PTRACE_SETREGS");
  puts("PTRACE_GETFPREGS");
  puts("PTRACE_SETFPREGS");
  puts("PTRACE_ATTACH");
  puts("PTRACE_DETACH");
  puts("PTRACE_GETFPXREGS");
  puts("PTRACE_SETFPXREGS");
  puts("PTRACE_SYSCALL");
  puts("PTRACE_SETOPTIONS");
  puts("PTRACE_GETEVENTMSG");
  if (argc > 1) ptrace(PTRACE_POKETEXT, 0, 0, 0);
  return 0;
}
