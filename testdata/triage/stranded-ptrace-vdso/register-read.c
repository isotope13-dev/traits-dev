void read_regs(int pid, void *iov) { ptrace(PTRACE_GETREGSET, pid, NT_PRSTATUS, iov); }
