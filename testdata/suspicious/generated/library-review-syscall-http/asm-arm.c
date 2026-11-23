void launch(void) { const char *s = "/bin/sh"; asm("mov x8, #221\n" "svc #0" : : "r"(s)); }
