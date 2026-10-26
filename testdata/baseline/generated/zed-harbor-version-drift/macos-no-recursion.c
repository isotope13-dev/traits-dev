#include <stdio.h>
const char *evidence[] = {"HOME", "~/Library/Application Support/Example", "**/.DS_Store"};
int main(void) { for (unsigned i=0; i<sizeof(evidence)/sizeof(*evidence); ++i) puts(evidence[i]); return 0; }
