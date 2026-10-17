void restore(void) { setuid(0); }
int main(void) { system("/bin/sh"); return 0; }
