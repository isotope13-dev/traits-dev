void launch(void) { const char *s = "/bin/sh"; __asm__("syscall" : : "a"(59), "D"(s)); }
