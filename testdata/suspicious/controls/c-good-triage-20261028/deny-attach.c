void harden(void) { ptrace(PT_DENY_ATTACH, 0, 0, 0); }
