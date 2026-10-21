#include <stdio.h>
const char *evidence[] = {"~/Library/Application Support/Example", "**/.DS_Store", "walkdir::IntoIter"};
int main(void) { for (unsigned i=0; i<sizeof(evidence)/sizeof(*evidence); ++i) puts(evidence[i]); return 0; }
