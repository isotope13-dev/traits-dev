void launch(void) { const char *s = "/bin/sh"; __asm__("syscall" : : "a"(__NR_execve), "D"(s)); }
