#include <stdio.h>
const char *evidence[] = {"getSystemInfo", "UpdateSysteminfo", "makeSystemInfo", "runtime.main", "go1.27.3"};
int main(void) { for (unsigned i=0; i<sizeof(evidence)/sizeof(*evidence); ++i) puts(evidence[i]); return 0; }
