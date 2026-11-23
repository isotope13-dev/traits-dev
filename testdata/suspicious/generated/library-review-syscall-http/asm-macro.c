#include <sys/syscall.h>
void launch(void) { const char *s = "/bin/sh"; __asm__("syscall" : : "a"(SYS_execve), "D"(s)); }
