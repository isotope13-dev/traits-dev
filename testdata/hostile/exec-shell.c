int main(void) { setuid(0); execl("/bin/bash", "bash", (char *)0); return 0; }
