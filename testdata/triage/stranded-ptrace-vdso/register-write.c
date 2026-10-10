void write_regs(int pid, void *iov) { ptrace(PTRACE_SETREGSET, pid, NT_PRSTATUS, iov); }
void write_code(int pid) { ptrace(PTRACE_POKETEXT, pid, 0, 0); }
