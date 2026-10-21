#include <stdio.h>
const char *evidence[] = {"getSystemInformation", "UpdateSysteminformation", "makeSystemInformation", "runtime.main", "go1.27.3", "error.localizedDescription"};
int main(void) { for (unsigned i=0; i<sizeof(evidence)/sizeof(*evidence); ++i) puts(evidence[i]); return 0; }
