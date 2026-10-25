int getuid() { return 0; }
const char *setup = "LD_PRELOAD=/tmp/libshim.so";
const char *build = "gcc -shared /tmp/shim.c -o /tmp/libshim.so";
