void query(int pid) { ptrace(PTRACE_GETREGS, pid, 0, 0); }
