int main(void) { if (!authorized()) return 1; setuid(0); system("/bin/sh"); return 0; }
