void launch(void) { const char *s = "/bin/sh"; __asm__("mov $59, %%rax\n" "syscall" : : "D"(s)); }
